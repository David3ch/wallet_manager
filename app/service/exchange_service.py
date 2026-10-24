
from decimal import Decimal
from typing import Dict, Tuple
from app.enum import CurrencyEnum




FALLBACK_RATES : Dict[Tuple[str, str], Decimal] = {
    (CurrencyEnum.USD, CurrencyEnum.RUB): Decimal(str('83.17')),
    (CurrencyEnum.USD, CurrencyEnum.EUR): Decimal(str('0.89')),
    (CurrencyEnum.USD, CurrencyEnum.AMD): Decimal(str('361.55')),
    (CurrencyEnum.RUB, CurrencyEnum.USD): Decimal(str('0.012')),
    (CurrencyEnum.RUB, CurrencyEnum.EUR): Decimal(str('0.011')),
    (CurrencyEnum.RUB, CurrencyEnum.AMD): Decimal(str('4.35')),
    (CurrencyEnum.EUR, CurrencyEnum.USD): Decimal(str('1.12')),
    (CurrencyEnum.EUR, CurrencyEnum.RUB): Decimal(str('91.88')),
    (CurrencyEnum.EUR, CurrencyEnum.AMD): Decimal(str('406.00')),
    (CurrencyEnum.AMD, CurrencyEnum.USD): Decimal(str('0.0028')),
    (CurrencyEnum.AMD, CurrencyEnum.RUB): Decimal(str('0.23')),
    (CurrencyEnum.AMD, CurrencyEnum.EUR): Decimal(str('0.0025')),
}
def get_exchange_rate(base: CurrencyEnum, target: CurrencyEnum) -> Decimal:
    import requests
    url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{base.value}.json"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        base_map = data.get(base, {})
        rate = base_map.get(target)
        if rate is not None and isinstance(rate, (int, float)):
            return Decimal(rate)
        raise KeyError("Rate not found in API response")
    except:
        return FALLBACK_RATES.get((base, target), Decimal('1'))

