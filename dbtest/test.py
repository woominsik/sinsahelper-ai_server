from ai_model import reference_by_url

if __name__ == '__main__':
    url = 'https://store.musinsa.com/app/goods/1906521'
    scores = reference_by_url(url)
    print(scores)