Setting up **Immich** to index an existing external hard drive without moving or messing up your files requires using its **"External Library"** feature. This allows Immich to "read-only" scan your drive while keeping your folder structure exactly how it is.

Since you likely use Windows (based on your previous SQL/VS Code questions), these steps are tailored for **Windows with Docker Desktop**.

### Phase 1: The Engine (Docker)

Immich is complex under the hood (database, machine learning, redis, etc.), so it runs inside containers.

1. **Download & Install Docker Desktop:** Go to [docker.com](https://www.docker.com/products/docker-desktop/) and install it.
    
2. **Start Docker:** Run it and wait for the whale icon in your taskbar to stop animating.
    
3. **Verify:** Open PowerShell and type `docker --version`. If it replies with a version number, you are ready.
    

---

### Phase 2: The Setup

1. **Create a Folder:** Create a folder on your C: drive (or wherever you want the _app_ to live, not the photos) called `immich-app`.
    
    - Example: `C:\immich-app`
        
2. Download Configuration Files:
    
    You need two specific text files. You can download them manually or use these PowerShell commands inside your immich-app folder:
    
    PowerShell
    
    ```
    Invoke-WebRequest https://github.com/immich-app/immich/releases/latest/download/docker-compose.yml -OutFile docker-compose.yml
    Invoke-WebRequest https://github.com/immich-app/immich/releases/latest/download/.env -OutFile .env
    ```
    

---

### Phase 3: The "Wiring" (Crucial Step)

This is where we tell Immich where your external hard drive is.

- _Assumption:_ Your external drive is **D:** and your photos are in **D:\MyArchive**.
    

1. **Open `docker-compose.yml`** in VS Code (or Notepad).
    
2. You need to add a line to **two** sections: `immich-server` and `immich-microservices`.
    
3. Look for the `volumes:` block in both sections. It usually looks like this:
    
    YAML
    
    ```
    volumes:
      - ${UPLOAD_LOCATION}:/usr/src/app/upload
      - /etc/localtime:/etc/localtime:ro
    ```
    
4. **Add your external drive mapping** to that list in **BOTH** sections.
    
    - Format: `- "WINDOWS_PATH:LINUX_MOUNT_POINT:ro"`
        
    - `ro` stands for Read-Only (Safety measure: Immich can't accidentally delete your files).
        
    
    **It should look like this after editing:**
    
    YAML
    
    ```
    # In immich-server section:
    volumes:
      - ${UPLOAD_LOCATION}:/usr/src/app/upload
      - /etc/localtime:/etc/localtime:ro
      - "D:\MyArchive:/mnt/media/hdd:ro"  <-- ADD THIS LINE
    
    # ... scroll down to immich-microservices section ...
    
    # In immich-microservices section:
    volumes:
      - ${UPLOAD_LOCATION}:/usr/src/app/upload
      - /etc/localtime:/etc/localtime:ro
      - "D:\MyArchive:/mnt/media/hdd:ro"  <-- ADD THIS SAME LINE
    ```
    
5. **Save the file.**
    

---

### Phase 4: The Launch

1. Open PowerShell and navigate to your folder: `cd C:\immich-app`
    
2. Run the command to start the engine:
    
    PowerShell
    
    ```
    docker compose up -d
    ```
    
3. **Wait.** It will download a few GBs of AI models and databases. This might take 5-10 minutes.
    
4. Once the text stops scrolling and it says "Started", open your web browser.
    
5. Go to: `http://localhost:2283`
    

---

### Phase 5: The Connection (Web UI)

1. **Create Admin Account:** Click "Getting Started" and make your admin user.
    
2. **Dark Mode:** (Optional, but highly recommended).
    
3. **Connect the Drive:**
    
    - Click the **Administration** button (usually top right).
        
    - Click **External Libraries** in the settings menu.
        
    - Click **Create Library**.
        
    - **Type:** Select "External".
        
    - **Import Paths:** Click the `...` or type the _Linux Mount Point_ you created in Phase 3.
        
    - Type exactly: `/mnt/media/hdd` (or whatever you put on the right side of the colon in step 3).
        
    - Click **Create**.
        
    - Click the **"Scan All Libraries"** button (or the refresh icon).
        

### What happens next?

- **Indexing:** Immich will crawl that folder structure.
    
- **Machine Learning:** You will see a "Jobs" tab in Administration. It will start queueing up "Face Detection," "Smart Search," and "Thumbnail Generation."
    
- **Results:** Depending on how many photos you have (e.g., 50k+), this will take **hours or days**. Keep the computer on. Once done, you can type "Dog in snow" and it will find the files on your D: drive instantly.