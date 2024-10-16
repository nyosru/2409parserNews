#
#creat: creat_caddyfile
#
#creat_caddyfile: ./../upr_serv/storage/app/caddy/777example.txt ./../upr_serv/storage/app/caddy/777example.txt
#	cat &^ > output_file.txt

ca:
	docker-compose up -d
	docker cp upr_serv:/home/upr_serv/storage/app/Caddyfile-new ./Caddyfile-new
	#docker-compose down
	#docker cp ./Caddyfile-new caddy:/etc/caddy/Caddyfile
	#docker cp ./Caddyfile-new /2304bu_serv-docker/caddy/Caddyfile
	#cp ./Caddyfile-new /2304bu_serv-docker/caddy/Caddyfile
	#cp ./Caddyfile-new /etc/caddy/Caddyfile
	cp ./Caddyfile-new ./caddy/Caddyfile
	cp ./Caddyfile-new ./caddy/Caddyfile.new
	#docker cp ./Caddyfile-new caddy:/etc/caddy/Caddyfile
	#docker cp ./Caddyfile-new caddy:/caddy/Caddyfile
	#cp docker-compose.local.yml docker-compose.yml
#	cp caddy/Caddyfile.new caddy/Caddyfile
	docker-compose up -d
	#cp caddy/dev.Caddyfile caddy/Caddyfile
	#make caddy_refresh_cfd
	#docker-compose up -d

d:
	# пересборка питон парсера web_scraper2
	docker-compose up -d --build --force-recreate web_scraper2
	#docker-compose -f ./docker-compose.local.yml up -d --remove-orphans

dev:
	cp caddy/dev.Caddyfile caddy/Caddyfile
	#cp caddy/dev.Caddyfile caddy2/Caddyfile
	cp docker-compose.local.yml docker-compose.yml
	docker-compose up -d --remove-orphans
	# использовать другой файл докер композ
	#docker-compose -f ./docker-compose.local.yml up -d --remove-orphans
	#docker-compose up -d --force-recreate web_scraper --remove-orphans
	make start_2309livewire
	#make start_base12narek_dev

	make caddy_refresh_cfd



# cp caddy/prod.Caddyfile caddy/Caddyfile
# cp docker-compose.prod.yml docker-compose.yml
#docker-compose up -d --build

#	make start_2309livewire
#	make start_2308beget_dev
#	make start_base17

#	make start_test231012
#	make start_2302didrive
# make start_2401test

#make start_as_didrive
#make start_as

#	make start_avtoas
#	#make start_avtoas_prod
#	make start_avtoas_didrive
#	#make start_avtoas_didrive_prod


#	make start_2308beget_dev
#	make start_base17
# make start_base16sites

# docker exec 2309larawire composer i
# docker exec 2309larawire php artisan migrate

# docker exec ttt72 composer i
# docker exec ttt72 php artisan migrate

# docker exec base17 composer i
# docker exec base17 php artisan migrate
# # docker exec base17_node npm i
# # docker exec base17 npm i

# docker exec sym_test composer i
# docker exec sym_test symfony -h
# docker exec sym_test php composer i



prod:
	cp caddy/prod.Caddyfile caddy/Caddyfile
	#cp caddy/prod.Caddyfile caddy2/Caddyfile
	cp docker-compose.prod.yml docker-compose.yml
	#docker-compose up -d --build --remove-orphans --no-recreate caddy
	docker-compose up -d --build --remove-orphans
	#docker-compose up -d --build
	#make start_2309livewire
	#make start_base12narek
	make caddy_refresh_cfd
	#docker system prune --force

# cp bu72_front/code/nuxt.config.prod.ts bu72_front/code/nuxt.config.ts
#	make start
#make start_2309livewire_prod
#	make start_test231012_prod

# рабочие

#	make start_2308beget
#	make start_2401test
#
#	make start_avtoas
#	make start_avtoas_prod
#	make start_avtoas_didrive
#
#	make start_base16sites
#	make start_base17

#	make start_base12narek
#	make start_site_api








start:
	make caddy_refresh_cfd
	make start_2308beget
	make start_2309livewire

#	docker exec ttt72_laravel composer i --no-dev
#	docker exec ttt72_laravel php artisan migrate

#	docker exec base17 composer i --no-dev
#	docker exec base17 php artisan migrate
# docker exec base17 npm i

start_base12narek:
	#docker exec 2308beget composer update
	docker exec base12narek composer i --no-dev
#	docker exec 2308beget composer i
	docker exec base12narek php artisan migrate
	docker exec base12narek chown -R www-data:www-data storage
	#docker exec base12narek npm run prod
	#docker exec base12narek npm run prod -- --skip-errors
	#docker exec base12narek npm run prod -- --no-clean
	#docker exec base12narek npm run dev



start_base12narek_dev:
	#docker exec 2308beget composer update
	docker exec base12narek composer i
#	docker exec 2308beget composer i
	docker exec base12narek php artisan migrate
	docker exec base12narek npm run dev
	#docker exec base12narek chown -R www-data:www-data storage

start_site_api:
	docker exec site_api composer i --no-dev

start_2308beget:
	#docker exec 2308beget composer update
	docker exec 2308beget composer i --no-dev
#	docker exec 2308beget composer i
	docker exec 2308beget php artisan migrate
	#docker exec 2308beget npm run build
	docker exec 2308beget chown -R www-data:www-data storage

start_2308beget_dev:
	docker exec 2308beget composer i
	docker exec 2308beget php artisan migrate
	#docker exec 2308beget npm run build
	#docker exec 2308beget php artisan storage:link


start_base17:
	docker exec base17 chown -R www-data:www-data storage
	docker exec base17 php composer.phar i
	#docker exec base17 composer i
	docker exec base17 php artisan migrate
	#docker exec base17 npm run build
	docker exec base17 npm i
	docker exec base17 npm run prod
	#docker exec base17 npm run dev
	#docker exec base17 npm run build

start_base16sites:
	#docker exec base16sites php composer.phar i --no-dev
	#docker exec base17 composer i
	#docker exec base17 npm run build
	#docker exec base16sites npm run prod

	docker exec base16sites composer i --no-dev
	docker exec base16sites php artisan migrate

start_2309livewire:
	docker exec 2309livewire composer i
	docker exec 2309livewire php artisan migrate
	docker exec 2309livewire chown -R www-data:www-data storage

start_test231012:
	docker exec test231012 composer i
	docker exec test231012 php artisan migrate
	docker exec test231012 php artisan l5-swagger:generate

start_test231012_prod:
	docker exec test231012 composer i --no-dev
	docker exec test231012 php artisan migrate
	docker exec test231012 php artisan l5-swagger:generate

start_2309livewire_prod:
	docker exec 2309livewire composer i --no-dev
	docker exec 2309livewire php artisan migrate

start_2302didrive:
	docker exec 2302didrive composer i
	docker exec 2302didrive php artisan migrate
	#docker exec 2302didrive php artisan l5-swagger:generate

start_2401test:
	docker exec 2401test composer i
	docker exec 2401test php artisan migrate
	docker exec 2401test chown -R www-data:www-data storage

start_2302didrive_prod:
	docker exec 2302didrive composer i --no-dev
	docker exec 2302didrive php artisan migrate
	docker exec 2302didrive php artisan l5-swagger:generate







#
#start_as_prod:
#	docker exec 2302didrive composer i --no-dev
#	docker exec 2302didrive php artisan migrate
#	docker exec 2302didrive php artisan l5-swagger:generate
#	docker exec 2312auto_as npx update-browserslist-db@latest
#	docker exec 2312auto_as npm run prod



#start_as:
#	docker exec 2312auto_as composer i
#	docker exec 2312auto_as php artisan migrate
#	docker exec 2312auto_as npx update-browserslist-db@latest
#	docker exec 2312auto_as npm run dev
#	#docker exec 2312auto_as npm run prod
#	#docker exec 2312auto_as php artisan l5-swagger:generate
#
#start_as_didrive:
#	docker exec 2312didrive_auto composer i
#	docker exec 2312didrive_auto php artisan migrate
#	#docker exec 2312didrive_auto php artisan l5-swagger:generate
#
#start_as_prod:
#	docker exec 2312auto_as composer i --no-dev
#	docker exec 2312auto_as php artisan migrate
#	docker exec 2312auto_as npx update-browserslist-db@latest
#	docker exec 2312auto_as npm run prod
#	#docker exec 2312auto_as php artisan l5-swagger:generate
#start_as_didrive_prod:
#	docker exec 2312didrive_auto composer i --no-dev
#	docker exec 2312didrive_auto php artisan migrate
#	#docker exec 2312didrive_auto php artisan l5-swagger:generate


start_avtoas:
	docker exec 2312auto_as composer i
	docker exec 2312auto_as php artisan migrate
	#docker exec 2312auto_as npx update-browserslist-db@latest
	#docker exec 2312auto_as npm run dev
	#docker exec 2312auto_as chmod -R 0777 storage
	docker exec 2312auto_as php artisan storage:link
start_avtoas_prod:
	docker exec 2312auto_as_prod composer i --no-dev
	docker exec 2312auto_as_prod php artisan migrate
	docker exec 2312auto_as_prod npx update-browserslist-db@latest

	docker exec 2312auto_as_prod npm i
	docker exec 2312auto_as_prod npm audit fix --force
	docker exec 2312auto_as_prod npm run prod

	#docker exec 2312auto_as_prod chmod -R 0777 storage
	docker exec 2312auto_as_prod php artisan storage:link

start_avtoas_didrive:
	#docker exec 2312didrive_auto chmod -R 0777 storage
	docker exec 2312didrive_auto composer i
	docker exec 2312didrive_auto php artisan migrate
	#docker exec 2312didrive_auto npx update-browserslist-db@latest
	#docker exec 2312didrive_auto npm run dev
	#docker exec 2312didrive_auto php artisan storage:link
start_avtoas_didrive_prod:
	#docker exec 2312didrive_auto_prod chmod -R 0777 storage
	docker exec 2312didrive_auto_prod composer i --no-dev
	docker exec 2312didrive_auto_prod php artisan migrate
	#docker exec 2312didrive_auto_prod npx update-browserslist-db@latest
	#docker exec 2312didrive_auto_prod npm run prod
	docker exec 2312didrive_auto_prod php artisan storage:link





caddy_refresh_cfd:
	#docker exec -w /etc/caddy caddy caddy fmt
	docker exec -w /etc/caddy caddy caddy reload
	#docker exec -w /etc/caddy caddy2 caddy reload





start0:

	docker-compose exec ttt72_laravel php artisan storage:link
	docker-compose up -d

start00:

	# docker stop $(docker ps -a -q)
	# docker rm $(docker ps -a -q)

	# docker-compose up --build -d --remove-orphans
	docker-compose up -d

	# docker-compose exec bu72_back composer i
	# docker-compose exec bu72_back php artisan migrate

	# docker-compose exec ttt72_laravel ls 
	# docker-compose exec caddy restart caddy

	# docker-compose exec ttt72_laravel php composer.phar i --no-dev
	docker exec ttt72_laravel php composer.phar i --no-dev

	# docker-compose exec ttt72_laravel php artisan migrate
	docker exec ttt72_laravel php artisan migrate
	
	make caddy_refresh_cfd


dev00:

	cp caddy/dev.Caddyfile caddy/Caddyfile
	cp docker-compose.local.yml docker-compose.yml

	# # bu72
	# cp bu72_front/code/nuxt.config.local.ts bu72_front/code/nuxt.config.ts

	# make start
	# docker-compose up --build
	# docker-compose down
	# docker-compose up --build -d --remove-orphans
	# docker-compose up --abort-on-container-exit
	# docker-compose up --build -d
	docker-compose up -d

	# docker exec -w /etc/caddy caddy caddy fmt

	make caddy_refresh_cfd

	# # docker-compose exec ttt72_laravel ./vendor/bin/sail up

	# ttt72_laravel
	# docker-compose exec ttt72_laravel composer i
	# docker-compose exec ttt72_laravel php artisan migrate

restart-cron:
	#@echo "Stopping cron service..."
	#sudo service cron stop
	#docker exec cron-service service cron stop
	@echo "удаляем конфиги"
	docker exec cron-service rm -f /etc/cron.d/*
	@echo "Copying new configuration..."
	#sudo cp ./cron/my-crontab cron-service:/etc/cron.d/my-crontab
	docker cp ./cron/my-crontab cron-service:/etc/cron.d/my-crontab
	@echo "Starting cron service..."
	#sudo service cron start
	#docker exec cron-service service cron start
	docker exec cron-service service cron reload
	@echo "Cron service restarted with new configuration."