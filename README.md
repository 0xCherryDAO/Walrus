## Для использования

Для установки библиотеки pysui необходимо <a href="https://www.rust-lang.org/tools/install">скачать</a> Rust

Версия python - 3.11

## Конфиг

### Опциональные настройки:

`BLOCK_VISION_API_KEY`— для проверки, имеется ли уже Walrus Explorer NFT, чтобы не покупать, если уже куплено.

Апи ключ создавать <a href="https://dashboard.blockvision.org/overview"> тут </a> 

`TG_BOT_TOKEN` — токен телеграм бота для уведомлений. Можно оставить `TG_BOT_TOKEN = None`. Создать тут - @BotFather

`TG_USER_ID` — цифровой айди пользователя, куда будут приходить уведомления. Можно узнать тут - @userinfobot

### Настройки:
#### --- CEXs --- #
`WITHDRAW_FROM_OKX`— Вывод с ОКХ | Минимальный вывод с ОКХ 0.1 SUI и комиссия 0.06 SUI. | `min_sui_balance` — Если на кошельке баланс больше установленного, то вывод с ОКХ осуществляться не будет.

#### --- Testnet --- #
`FAUCET`— Получение токенов с крана

`SWAP`— Свап тестовых SUI на WAL

`STAKE`— Стейк WAL в рандомном пуле

`MINT_FLATLAND_NFT`— Минт FlatLand NFT

#### --- Mainnet --- #
`BUY_WALRUS_NFT` - Покупка Walrus Explorer NFT с маркета по флору.

## Установка и запуск
```bash
pip install -r requirements.txt

# Перед запуском необходимо настроить модули в config.py
python main.py
```