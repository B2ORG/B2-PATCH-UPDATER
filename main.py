import asyncio, sys
import config as cfg
from PatchUpdaterApp import PatchUpdaterApp
from PatchUpdaterRunner import PatchUpdaterRunner


async def main():
    print(f"B2-PATCH-UPDATER v{cfg.VERSION}{f" BETA" if cfg.VERSION.startswith("0") else ""}")
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    app = (PatchUpdaterApp()
                    .prepare_environment()
                    .load_config()
     )

    if "--config" in args:
        sys.exit(0)

    updater = (PatchUpdaterRunner(app)
                    .scan_files()
                    .get_update_info()
                    .set_downloader_attributes()
     )
    queue = updater.get_update_queue()
    if not len(queue):
        input("No updates found. Press any key to exit...")
        sys.exit(0)

    print(f"Fetching updates for {len(queue)} files")
    await updater.get_downloader().fetch_all()
    print("Finished downloading")
    updater.manage_downloaded()
    print(f"Finished updating, {updater.get_success()} files updated, {updater.get_fail()} files failed")
    input("Press any key to exit...")


if __name__ == "__main__":
    asyncio.run(main())
