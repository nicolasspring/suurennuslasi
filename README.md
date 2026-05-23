# suurennuslasi
Visualizing Instagram posts

# Access Token

In order to visualize your posts, you will need an access token with the necessary permissions. To obtain one, you can follow these steps:

1. Turn your Instagram account into a professional account (e.g. creator)
2. Create a Facebook page (e.g. a personal blog)
3. Link your Instagram account to the Facebook page
4. Create an app under https://developers.facebook.com with the *Manage messaging & content on Instagram* use case
5. Customize the use case to include the following permissions:
   1. business_management
   2. instagram_basic
   3. instagram_manage_comments
   4. instagram_manage_insights
   5. pages_read_engagement
   6. instagram_manage_contents
6. Go to the [Graph API Explorer](https://developers.facebook.com/tools/explorer/) and create an access token with these permissions
7. Create a file `.env` file at the repo root
8. Add the access token to the `.env` file

Your `.env` file should look like this:

````````
ACCESS_TOKEN=YOUR_TOKEN
````````

