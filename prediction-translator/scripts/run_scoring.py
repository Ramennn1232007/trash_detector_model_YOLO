from app.api.routes_signals import get_signals


if __name__ == "__main__":
    for signal in get_signals():
        print(signal)
