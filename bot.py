import requests
from bs4 import BeautifulSoup
import time

OLLAMA_API_URL = "http://localhost:11434"

def query_ollama_model(prompt):
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3.2:1b",
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(f"{OLLAMA_API_URL}/api/generate", json=data, headers=headers)
    return response.json()

def custom_google_search(query, num_results=3):
    try:
        # Format URL tìm kiếm Google
        search_url = f"https://www.google.com/search?q={query}&lr=lang_vi&num={num_results}"
        
        # Headers để giả lập trình duyệt
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Gửi request
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tìm các kết quả
        search_results = []
        for result in soup.find_all('div', class_='g'):
            link = result.find('a')
            title = result.find('h3')
            snippet = result.find('div', class_='VwiC3b')
            
            if link and title and snippet:
                search_results.append({
                    'url': link['href'],
                    'title': title.text,
                    'snippet': snippet.text
                })
            if len(search_results) >= num_results:
                break
            time.sleep(1)
                
        return search_results
    except Exception as e:
        return f"Lỗi khi tìm kiếm: {str(e)}"

def analyze_query_type(query):
    # Danh sách từ khóa cho câu hỏi cần tham khảo
    knowledge_keywords = [
        'là gì', 'định nghĩa', 'giải thích', 'thế nào',
        'cách', 'làm sao', 'ví dụ', 'trình bày', 'tổng hợp',
        'so sánh', 'khác nhau', 'tại sao', 'vì sao',
        'explain', 'lâu', 'hình thành', 
        'phát triển','tổng quan','tổng quát'
    ]
    
    # Danh sách từ khóa cho câu hỏi đơn giản
    simple_keywords = [
        'chào', 'hi', 'hello', 'bye', 'tạm biệt',
        'khỏe không', 'bạn tên gì','thế nào','vấn đề'
    ]
    
    query = query.lower()
    
    # Kiểm tra nếu là câu hỏi cần tham khảo
    for keyword in knowledge_keywords:
        if keyword in query:
            return "need_reference"
            
    # Kiểm tra nếu là câu hỏi đơn giản
    for keyword in simple_keywords:
        if keyword in query:
            return "simple_chat"
            
    # Mặc định cần tham khảo nếu không rơi vào các trường hợp trên
    return "need_reference"


def process_query(user_input):
    query_type = analyze_query_type(user_input)
    
    # Lấy câu trả lời từ model
    model_response = query_ollama_model(user_input)
    response = "🤖 \n"
    response += f"{model_response['response']}\n\n"
    
    # Chỉ thêm tham khảo nếu cần
    if query_type == "need_reference":
        search_results = custom_google_search(user_input)
        response += "📚 Nguồn tham khảo:\n"
        if isinstance(search_results, list):
            for i, result in enumerate(search_results, 1):
                response += f"\n{i}. <a href='{result['url']}' target='_blank'>{result['title']}</a>\n"

    return {"response": response}