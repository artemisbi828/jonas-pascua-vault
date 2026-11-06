Main ngrok commands:
	ngrok http [port] - Create HTTP tunnel (what you'll use most)
	ngrok tcp [port] - Create TCP tunnel
	ngrok version - Check version
	ngrok config check - Validate your config
	ngrok config edit - Edit configuration file

Common flags for ngrok http:

--domain [custom-domain] - Use a custom domain (paid feature)
--region [us|eu|ap|au|sa|jp|in] - Choose server region
--log stdout - Show logs in terminal

**WORKING NOTES**
ngrok config edit -- pulls up my yaml config file 
	location --> C:\Users\jpasc\AppData\Local\ngrok

1. terimnal 1 -- npm run dev
2. terminal 2 -- ngrok http 3000 (my port)
3. https://illiquid-journalish-june.ngrok-free.dev/marketing -- their domain base