[app]
title = Stock Fetcher
package.name = stockfetcher
package.domain = com.apal
source.include_exts = py,png,json
source.include_patterns = assets/*
icon.filename = assets/app_icon.png
version = 1.0.0

[buildozer]
log_level = 2

[requirements]
python_version = 3.10
requirements = flet, yfinance, pandas, numpy

[android]
package.name = stockfetcher
package.domain = com.yourname