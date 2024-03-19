import requests
from bs4 import BeautifulSoup
import openai

# 設定OpenAI API密鑰
openai.api_key = 'API密鑰'


def get_news(url):
    request = requests.get(url)
    data = BeautifulSoup(request.text, "html.parser")
    contents = data.find_all('div', class_='field-item even')

    all_paragraphs = []

    # 內容在div為'field-item even'的所有<p>中
    for content in contents:
        paragraphs = content.find_all('p')
        for p in paragraphs:
            all_paragraphs.append(p.get_text(strip=True))

    text = ' '.join(all_paragraphs)
    return text


def summarize_news(content):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "以下是新聞內容，幫我用150字以內總結"},
                {"role": "user", "content": content}
            ],
            temperature=0.5,
            max_tokens=200,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"


# run
url = 'https://www.ithome.com.tw/news/152373'
news_content = get_news(url)
#print('所有內容： \n',news_content)
news_summary = summarize_news(news_content)
print('新聞內容總結： \n',news_summary)
