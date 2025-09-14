from dotenv import load_dotenv
import os 
import requests
from urllib.parse import quote
import time
import concurrent.futures
load_dotenv()
from snapshot_Operations import poll_snapshot_status, download_snapshot

def _make_api_request(url, timeout=20, **kwargs):
    """Optimized API request with timeout and retry logic"""
    api_key = os.getenv("BRIGHTDATA_API_KEY")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, timeout=timeout, **kwargs)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print(f"⏰ API request timed out after {timeout}s")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ API request error: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

def serp_search(query, engine="google", timeout=15):
    """Optimized SERP search with timeout"""
    start_time = time.time()
    
    if engine == "google":
        base_url = "https://www.google.com/search"
    elif engine == "bing":
        base_url = "https://www.bing.com/search"
    else:
        raise ValueError("Unsupported search engine")
    
    url = "https://api.brightdata.com/request"

    # 🚀 Optimized payload - reduce data size
    payload = {
        "zone": "ai_research_agent",
        "url": f"{base_url}?q={quote(query)}&brd_json=1&num=10",  # Limit to 10 results
        "format": "raw"
    }

    full_response = _make_api_request(url, timeout=timeout, json=payload)
    
    elapsed = time.time() - start_time
    print(f"🔍 {engine.capitalize()} search: {elapsed:.1f}s")

    if not full_response:
        return {"knowledge": {}, "organic": [], "timeout": True}
    
    # 🚀 Extract only essential data to reduce processing time
    extracted_data = {
        "knowledge": full_response.get("knowledge", {}),
        "organic": full_response.get("organic", [])[:8],  # Limit to top 8 results
    }

    return extracted_data

def _trigger_and_download_snapshot_fast(trigger_url, params, data, operation_name="operation", timeout=25):
    """Fast snapshot handling with timeout"""
    start_time = time.time()
    
    # 🚀 Trigger with timeout
    trigger_result = _make_api_request(trigger_url, timeout=timeout, params=params, json=data)
    if not trigger_result:
        print(f"❌ {operation_name} trigger failed")
        return None 
    
    snapshot_id = trigger_result.get("snapshot_id")
    if not snapshot_id:
        print(f"❌ No snapshot ID for {operation_name}")
        return None
    
    # 🚀 Fast polling with shorter intervals
    if not poll_snapshot_status_fast(snapshot_id, max_wait=timeout):
        print(f"⏰ {operation_name} snapshot timed out")
        return None

    raw_data = download_snapshot(snapshot_id)
    
    elapsed = time.time() - start_time
    print(f"⚡ {operation_name} completed: {elapsed:.1f}s")
    
    return raw_data

def poll_snapshot_status_fast(snapshot_id, max_wait=25, check_interval=2):
    """Fast polling with aggressive timeouts"""
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        status = poll_snapshot_status(snapshot_id)
        if status:  # Snapshot ready
            return True
        time.sleep(check_interval)  # Check every 2 seconds instead of 5
    
    print(f"⏰ Snapshot {snapshot_id} timed out after {max_wait}s")
    return False

# 🚀 OPTIMIZED: Faster Reddit search with quality focus
def reddit_search_api(keyword, date="All time", sort_by="Top", num_of_posts=12):
    """Optimized Reddit search - fewer posts, higher quality"""
    trigger_url = "https://api.brightdata.com/datasets/v3/trigger"

    params = {
        "dataset_id": "gd_lvz8ah06191smkebj4",
        "include_errors": "true",
        "type": "discover_new",
        "discover_by": "keyword"
    }

    # 🚀 Reduced posts for speed, "Top" for quality
    data = [
        {
            "keyword": keyword,
            "date": date,
            "sort_by": sort_by,  # "Top" gives better quality than "Hot"
            "num_of_posts": num_of_posts,  # Reduced from 25 to 12
        }
    ]

    raw_data = _trigger_and_download_snapshot_fast(
        trigger_url, params, data, 
        operation_name="Reddit search", 
        timeout=20  # 20s timeout for Reddit search
    )

    if not raw_data:
        return {"parsed_data": [], "total_posts": 0}
    
    parsed_data = []
    for post in raw_data:
        if isinstance(post, dict):
            parsed_post = {
                "title": post.get("title"),
                "url": post.get("url"),
                "score": post.get("score", 0),  # Add score for quality ranking
                "num_comments": post.get("num_comments", 0),  # Add comment count
                "subreddit": post.get("subreddit", ""),  # Add subreddit info
            }
            parsed_data.append(parsed_post)

    # 🚀 Sort by engagement (score + comments) for quality
    parsed_data.sort(key=lambda x: (x.get("score", 0) + x.get("num_comments", 0)), reverse=True)
    
    return {"parsed_data": parsed_data, "total_posts": len(parsed_data)}

# 🚀 OPTIMIZED: Fast Reddit post retrieval with limits
def reddit_post_retrieval(urls, days_ago=0, load_all_replies=False, comment_limit=20):
    """Fast Reddit post retrieval with strict limits"""
    if not urls:
        return {"parsed_comments": [], "total_comments": 0}
    
    # 🚀 Limit to top 3 URLs for speed
    limited_urls = urls[:3]
    print(f"📱 Retrieving {len(limited_urls)} Reddit posts...")
    
    trigger_url = "https://api.brightdata.com/datasets/v3/trigger"

    params = {
        "dataset_id": "gd_lvzdpsdlw09j6t702",
        "include_errors": "true",
        "type": "discover_new",
        "discover_by": "url",
    }

    # 🚀 Process URLs with comment limits for speed
    data = [
        {
            "url": url,
            "days_ago": days_ago,
            "load_all_replies": load_all_replies,
            "comment_limit": comment_limit  # Limit comments per post
        }
        for url in limited_urls
    ]

    raw_data = _trigger_and_download_snapshot_fast(
        trigger_url, params, data, 
        operation_name="Reddit posts", 
        timeout=15  # 15s timeout for post retrieval
    )

    if not raw_data:
        return {"parsed_comments": [], "total_comments": 0}
    
    parsed_comments = []

    for comment in raw_data:
        if isinstance(comment, dict):
            # 🚀 Extract only essential comment data
            parsed_comment = {
                "comment_id": comment.get("comment_id"),
                "content": comment.get("comment"),
                "date": comment.get("date_posted"),
                "score": comment.get("score", 0),  # Add score for quality
            }
            parsed_comments.append(parsed_comment)
    
    # 🚀 Sort comments by score and limit to top comments
    parsed_comments.sort(key=lambda x: x.get("score", 0), reverse=True)
    top_comments = parsed_comments[:50]  # Limit to top 50 comments
    
    return {"parsed_comments": top_comments, "total_comments": len(top_comments)}

# 🚀 NEW: Parallel search function for maximum speed
def parallel_search_all_sources(query, timeout_per_search=15):
    """Run all searches in parallel for maximum speed"""
    
    def search_google():
        try:
            return ("google", serp_search(query, engine="google", timeout=timeout_per_search))
        except Exception as e:
            print(f"❌ Google search failed: {e}")
            return ("google", {"knowledge": {}, "organic": [], "error": str(e)})
    
    def search_bing():
        try:
            return ("bing", serp_search(query, engine="bing", timeout=timeout_per_search))
        except Exception as e:
            print(f"❌ Bing search failed: {e}")
            return ("bing", {"knowledge": {}, "organic": [], "error": str(e)})
    
    def search_reddit():
        try:
            return ("reddit", reddit_search_api(query))
        except Exception as e:
            print(f"❌ Reddit search failed: {e}")
            return ("reddit", {"parsed_data": [], "total_posts": 0, "error": str(e)})
    
    print("🚀 Starting parallel searches...")
    start_time = time.time()
    
    # 🚀 Run all searches in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(search_google),
            executor.submit(search_bing),
            executor.submit(search_reddit)
        ]
        
        results = {}
        for future in concurrent.futures.as_completed(futures, timeout=25):  # 25s total timeout
            try:
                source, data = future.result()
                results[f"{source}_results"] = data
            except Exception as e:
                print(f"❌ Search error: {e}")
    
    total_time = time.time() - start_time
    print(f"⚡ All searches completed in {total_time:.1f}s")
    
    return results









