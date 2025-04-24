import requests
import os # Import os module

url = "http://192.168.2.102:50000/tts_inter"
output_filename = "received_audio.wav" # Define the output filename

# Define the text you want to send to the TTS API
text_to_speak = "宝贝们别担心，咱们罗马仕充电宝可是有7天无理由退货的，还自带运费险！买贵了？不存在的，直播间专属优惠价给你安排上今天下单的宝宝更有福利哦，评论区打'已拍'立马送你原装数据线！发货速度也是杠杠的，早上下单可能当天就能发出，最晚第二天也给你安排得明明白白。偏远地区的小可爱们也不用等太久，两三天就能到手啦，全国联保加一年质保。这售后你说香不香？"

# Prepare the parameters for the request
# requests will handle URL encoding (e.g., spaces to %20)
request_params = {"tts_text": text_to_speak}

try:
    print(f"Sending request to: {url} with text: '{text_to_speak}'")
    # Send GET request with the parameters
    response = requests.get(url, params=request_params)

    # 檢查狀態碼是否為 200 (OK)
    if response.status_code == 200:
        print("請求成功！")
        # 檢查內容類型是否為 audio/wav
        # 使用 .get() 方法來避免如果 'content-type' 缺失時出現錯誤
        content_type = response.headers.get('content-type', '')
        if 'audio/wav' in content_type:
            print(f"Received WAV audio. Saving to {output_filename}...")
            # 開啟輸出文件以二進制寫入模式 ('wb')
            try:
                with open(output_filename, 'wb') as f:
                    # 將接收到的字節 (response.content) 寫入文件
                    f.write(response.content)
                print(f"Audio saved successfully to {os.path.abspath(output_filename)}")
            except IOError as e:
                print(f"Error saving file: {e}")
        else:
            # 處理意外的內容類型
            print(f"Error: Expected 'audio/wav' content type, but received '{content_type}'")
            print("原始回應內容：")
            print(response.text) # 印出原始文字內容
    else:
        # 如果狀態碼不是 200，印出錯誤訊息和狀態碼
        print(f"請求失敗，狀態碼：{response.status_code}")
        print("伺服器回應：")
        print(response.text) # 印出原始文字內容，有助於除錯

except requests.exceptions.RequestException as e:
    # 處理 requests 可能發生的錯誤 (例如連線問題)
    print(f"請求發生錯誤：{e}")

