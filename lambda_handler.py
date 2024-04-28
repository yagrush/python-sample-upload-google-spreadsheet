from src import __main__


def lambda_handler(event, context):
    print(event) # POSTのbodyが渡ってくる 例）{"hogehoge": "fuga"}
    print(event.keys())
    __main__.main([])