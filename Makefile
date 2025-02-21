all: clean build

build: build-main build-config

build-main: mo
	pyinstaller --distpath dist/linux --workpath build/linux \
	--clean --onefile --hidden-import coloredlogs -p . -c -n transmission-rutracker-seed \
	--add-data transmission_rutracker_seed/locale:transmission_rutracker_seed/locale \
	--add-data LICENSE:LICENSE \
	bin/main.py

build-config: mo
	pyinstaller --distpath dist/linux --workpath build/linux \
	--clean --onefile --hidden-import coloredlogs -p . -c -n transmission-rutracker-seed-config \
	--add-data transmission_rutracker_seed/config/views/index.tpl:transmission_rutracker_seed/config/views \
	--add-data transmission_rutracker_seed/config/static/bootstrap/css/bootstrap.min.css:transmission_rutracker_seed/config/static/bootstrap/css \
	--add-data transmission_rutracker_seed/config/static/bootstrap/css/bootstrap-theme.min.css:transmission_rutracker_seed/config/static/bootstrap/css \
	--add-data transmission_rutracker_seed/locale:transmission_rutracker_seed/locale \
	--add-data LICENSE:LICENSE \
	bin/config.py

clean:
	rm -rf build

pot:
	mkdir -p build
	PYTHONPATH=$$(pwd) pybabel extract -w 120 -o build/po.pot -F babel.cfg transmission_rutracker_seed

po:	pot
	pybabel update -d transmission_rutracker_seed/locale -w 120 --init-missing -l ru -i build/po.pot

mo:
	find . -name \*.po -execdir msgfmt -f -o messages.mo messages.po \;

win-deps:
	WINEPREFIX=$$(realpath .wine) wine python -m pip install -r requirements.release.txt

build-win-main: win-deps mo
	WINEPREFIX=$$(realpath .wine) wine python -m PyInstaller --distpath dist/win --workpath build/win --upx-dir c:/upx/ \
	--clean --onefile --hidden-import coloredlogs -p . -c -n transmission-rutracker-seed \
	--add-data transmission_rutracker_seed/locale:transmission_rutracker_seed/locale \
	--add-data LICENSE:LICENSE \
	bin/main.py

build-win-config: win-deps mo
	WINEPREFIX=$$(realpath .wine) wine python -m PyInstaller --distpath dist/win --workpath build/win --upx-dir c:/upx/ \
	--clean --onefile --hidden-import coloredlogs -p . -c -n transmission-rutracker-seed-config \
	--add-data transmission_rutracker_seed/config/views/index.tpl:transmission_rutracker_seed/config/views \
	--add-data transmission_rutracker_seed/config/static/bootstrap/css/bootstrap.min.css:transmission_rutracker_seed/config/static/bootstrap/css \
	--add-data transmission_rutracker_seed/config/static/bootstrap/css/bootstrap-theme.min.css:transmission_rutracker_seed/config/static/bootstrap/css \
	--add-data transmission_rutracker_seed/locale:transmission_rutracker_seed/locale \
	--add-data LICENSE:LICENSE \
	bin/config.py

build-win: build-win-main build-win-config
