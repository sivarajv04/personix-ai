from pathlib import Path

ROOT = Path("personix-frontend/src")

folders = [
    "app",
    "assets/images",
    "assets/icons",
    "assets/styles",

    "api",

    "components/ui",
    "components/layout",
    "components/feedback",

    "features/landing/pages",
    "features/landing/sections",

    "features/orders/pages",
    "features/orders/components",
    "features/orders/hooks",

    "features/bulk/pages",
    "features/bulk/components",

    "features/admin/pages",
    "features/admin/components",
    "features/admin/hooks",

    "routes",
    "utils"
]

files = [
    "app/App.jsx",
    "app/router.jsx",
    "app/providers.jsx",

    "api/client.js",
    "api/dataset.api.js",
    "api/bulk.api.js",
    "api/admin.api.js",

    "features/landing/pages/Home.jsx",

    "features/orders/pages/OrderPage.jsx",
    "features/orders/pages/TrackPage.jsx",
    "features/orders/pages/DownloadPage.jsx",

    "features/bulk/pages/BulkRequest.jsx",

    "features/admin/pages/Dashboard.jsx",
    "features/admin/pages/Inventory.jsx",
    "features/admin/pages/Requests.jsx",
    "features/admin/pages/Analytics.jsx",

    "routes/publicRoutes.jsx",
    "routes/portalRoutes.jsx",
    "routes/adminRoutes.jsx",

    "utils/constants.js",
    "utils/format.js",
    "utils/validators.js"
]

def create():
    for folder in folders:
        path = ROOT / folder
        path.mkdir(parents=True, exist_ok=True)

    for file in files:
        path = ROOT / file
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)

    print("✅ Personix React structure created successfully")

if __name__ == "__main__":
    create()
