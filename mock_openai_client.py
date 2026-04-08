from openai import OpenAI
import time
import sys
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import os

try:
    import psutil
except ImportError:
    psutil = None


def _rss_mb() -> float:
    if psutil is None:
        return 0.0
    return psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)


def _run_with_rss_stats(label, fn, *args, **kwargs):
    if psutil is None:
        print(f"[{label}] psutil not installed. Skipping RSS stats.")
        return fn(*args, **kwargs)

    baseline = _rss_mb()
    peak = baseline
    stop_event = threading.Event()

    def _monitor_rss():
        nonlocal peak
        while not stop_event.is_set():
            current = _rss_mb()
            if current > peak:
                peak = current
            time.sleep(0.02)

    monitor_thread = threading.Thread(target=_monitor_rss, daemon=True)
    monitor_thread.start()

    try:
        return fn(*args, **kwargs)
    finally:
        stop_event.set()
        monitor_thread.join(timeout=1.0)
        final = _rss_mb()
        print(
            f"[{label}] RSS baseline={baseline:.2f} MB | peak={peak:.2f} MB | "
            f"final={final:.2f} MB | peak_delta={peak - baseline:.2f} MB"
        )


def single_streaming_request(request_id):
    """Single streaming request - can be parallelized"""
    try:
        client = OpenAI(
            base_url="http://localhost:8002/v1",
            api_key="dummy"
        )
        
        start_time = time.time()
        bytes_written = 0
        
        with client.files.with_streaming_response.content("test-file-65") as response:
            for chunk in response.iter_bytes(chunk_size=1024 * 1024):
                bytes_written += len(chunk)

        elapsed = time.time() - start_time
        return {
            "id": request_id,
            "mode": "streaming",
            "bytes": bytes_written,
            "elapsed": elapsed,
            "success": True
        }
    except Exception as e:
        return {
            "id": request_id,
            "mode": "streaming",
            "success": False,
            "error": str(e)
        }


def single_non_streaming_request(request_id):
    """Single non-streaming request - can be parallelized"""
    try:
        client = OpenAI(
            base_url="http://localhost:8002/v1",
            api_key="dummy"
        )
        
        start_time = time.time()
        
        content = client.files.content("test-file-65")
        payload = content.content
        bytes_written = len(payload)

        elapsed = time.time() - start_time
        return {
            "id": request_id,
            "mode": "non-streaming",
            "bytes": bytes_written,
            "elapsed": elapsed,
            "success": True
        }
    except Exception as e:
        return {
            "id": request_id,
            "mode": "non-streaming",
            "success": False,
            "error": str(e)
        }


def load_test_streaming(num_workers):
    """Load test streaming mode with concurrent requests"""
    print(f"\n{'='*60}")
    print(f"LOAD TEST: STREAMING with {num_workers} concurrent requests")
    print(f"{'='*60}\n")
    
    start_time = time.time()
    results = []
    
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [
            executor.submit(single_streaming_request, i)
            for i in range(num_workers)
        ]
        
        # IMPORTANT: Wait for ALL futures to complete before processing
        # This keeps all data in memory simultaneously for true peak measurement
        for future in futures:
            results.append(future.result())
    
    # Now display results after all are collected
    for i, result in enumerate(results, 1):
        if result["success"]:
            print(f"  [{i}/{len(results)}] Request {result['id']}: {result['bytes'] / (1024*1024):.2f} MB in {result['elapsed']:.2f}s")
        else:
            print(f"  [{i}/{len(results)}] Request {result['id']}: FAILED - {result['error']}")
    
    total_time = time.time() - start_time
    successful = sum(1 for r in results if r["success"])
    total_bytes = sum(r["bytes"] for r in results if r["success"])
    
    print(f"\n  Summary:")
    print(f"    Total time: {total_time:.2f}s")
    print(f"    Successful: {successful}/{num_workers}")
    # print(f"    Total data: {total_bytes / (1024*1024):.2f} MB")
    if total_time > 0:
        print(f"    Throughput: {(total_bytes / (1024*1024*1024)) / total_time:.2f} GB/s")


def load_test_non_streaming(num_workers):
    """Load test non-streaming mode with concurrent requests"""
    print(f"\n{'='*60}")
    print(f"LOAD TEST: NON-STREAMING with {num_workers} concurrent requests")
    print(f"{'='*60}\n")
    
    start_time = time.time()
    results = []
    
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [
            executor.submit(single_non_streaming_request, i)
            for i in range(num_workers)
        ]
        
        # IMPORTANT: Wait for ALL futures to complete before processing
        # This keeps all data in memory simultaneously for true peak measurement
        for future in futures:
            results.append(future.result())
    
    # Now display results after all are collected
    for i, result in enumerate(results, 1):
        if result["success"]:
            print(f"  [{i}/{len(results)}] Request {result['id']}: {result['bytes'] / (1024*1024):.2f} MB in {result['elapsed']:.2f}s")
        else:
            print(f"  [{i}/{len(results)}] Request {result['id']}: FAILED - {result['error']}")
    
    total_time = time.time() - start_time
    successful = sum(1 for r in results if r["success"])
    total_bytes = sum(r["bytes"] for r in results if r["success"])
    
    print(f"\n  Summary:")
    print(f"    Total time: {total_time:.2f}s")
    print(f"    Successful: {successful}/{num_workers}")
    print(f"    Total data: {total_bytes / (1024*1024):.2f} MB")
    if total_time > 0:
        print(f"    Throughput: {(total_bytes / (1024*1024*1024)) / total_time:.2f} GB/s")


def load_test_both(num_workers):
    """Load test both modes with concurrent requests"""
    print(f"\n{'='*60}")
    print(f"LOAD TEST: COMPARING STREAMING vs NON-STREAMING")
    print(f"Concurrent requests per mode: {num_workers}")
    print(f"{'='*60}")
    
    load_test_streaming(num_workers)
    print()
    load_test_non_streaming(num_workers)
    
    print(f"\n{'='*60}")
    print("Profile with memray to see peak memory usage:")
    print(f"  memray run -o memray-load-test.bin mock_openai_client.py --load-test --workers {num_workers}")
    print(f"  memray flamegraph memray-load-test.bin")
    print(f"{'='*60}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load test streaming vs non-streaming file content")
    parser.add_argument("--streaming-load-test", action="store_true", help="Run load test for streaming mode only")
    parser.add_argument("--non-streaming-load-test", action="store_true", help="Run load test for non-streaming mode only")
    parser.add_argument("--workers", type=int, default=5, help="Number of concurrent requests for load testing (default: 5)")
    
    args = parser.parse_args()
    
    if args.streaming_load_test:
        _run_with_rss_stats(
            "streaming-load-test",
            load_test_streaming,
            args.workers,
        )
    elif args.non_streaming_load_test:
        _run_with_rss_stats(
            "non-streaming-load-test",
            load_test_non_streaming,
            args.workers,
        )
    else:
        parser.print_help()