import requests
import json
import os

def upload_file(api_key, file_path, user_id="abc-123"):
    """上传文件到 Dify"""
    upload_url = "http://localhost/v1/files/upload"
    
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    # 根据文件扩展名设置正确的 MIME 类型
    file_extension = os.path.splitext(file_path)[1].lower()
    mime_types = {
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.wav': 'audio/wav',
        '.mp3': 'audio/mpeg',
        '.txt': 'text/plain'
    }
    file_type = mime_types.get(file_extension, 'application/octet-stream')
    
    files = {
        'file': (
            os.path.basename(file_path),
            open(file_path, 'rb'),
            file_type
        )
    }
    
    data = {
        'user': user_id
    }
    
    response = requests.post(
        upload_url,
        headers=headers,
        files=files,
        data=data
    )
    
    # 修改成功状态码的判断
    if response.status_code in [200, 201]:  # 添加 201
        result = response.json()
        print(f"文件上传成功: {result}")
        return result.get('id')
    else:
        print(f"文件上传失败: {response.status_code}")
        print(response.text)
        return None

def call_dify_workflow(api_key, upload_file_id, document_type="document"):  # 修改默认类型为 document
    """调用 Dify 工作流"""
    url = "http://localhost/v1/workflows/run"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "inputs": {
            "file": {
                "transfer_method": "local_file",
                "upload_file_id": upload_file_id,
                "type": document_type
            }
        },
        "response_mode": "streaming",
        "user": "abc-123"
    }

    response = requests.post(url, headers=headers, json=payload, stream=True)
    
    if response.status_code == 200:
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                print(decoded_line)
    else:
        print(f"工作流调用失败: {response.status_code}")
        print(response.text)

def main():
    api_key = "app-UamR0VEy0CFoEmsF4a4al536"
    
    # 使用绝对路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "demo_doc", "Introducing computer use.docx")
    
    print(f"使用文件路径: {file_path}")
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"错误: 文件不存在: {file_path}")
        return
    
    # 1. 上传文件
    file_id = upload_file(api_key, file_path)
    if file_id:
        print(f"文件上传成功，ID: {file_id}")
        
        # 2. 调用工作流
        call_dify_workflow(api_key, file_id, document_type="document")
    else:
        print("文件上传失败，终止工作流调用")

if __name__ == "__main__":
    main()