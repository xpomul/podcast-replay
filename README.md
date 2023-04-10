# podcast-replay

A self-hosted proxy for podcast feeds that "re-releases" a backlog of episodes in a configurable interval.

## Service Description

This is a simple python web service that I have mainly implemented for myself to address the following issue:

I have found an interesting podcast with a backlog of over 10 years of weekly episodes, which I wanted to listen to 
one by one over the time to come. The problem is that I don't want to manage these episodes manually. Instead I wanted
for the episodes to be added to my podcatcher queue every 2-3 days, so I don't clutter my inbox and still catch up with the podcast
steadily over time.

This service does just that. It reads the feed from the original server, manipulates the publication dates of the episodes and just returns the modified feed.

The configuration is done in the `config/podcast-replay.json` file:

```json
{ 
    "TheAwesomePodcast" : {    // <- the name/ID of the podcast under which it can be retrieved from the service
        "url": "https://.../feed.xml", // <- the URL of the original podcast feed
        "skip": 10,                    // <- the number of episodes to skip from the start of the feed
        "date": "2023-04-01",          // <- the desired publication date of the first unskipped episode (in YY-MM-DD format)
        "rate": 2                      // <- the frequency in days between the publication of each episode  
    }
}
```

In this example, the podcast feed would be read, the first 10 episodes would be skipped, and the 11th episode would get the publication date of April 1st.

The 12th episode would get the publication date of April 3rd, and so on. Any episode with a publication date in the future is excluded from the feed. So, on April 4th, only the episodes 11 and 12 would be included; on April 5th, episode 13 would be added, and so on.

To access the transformed feed for the podcast configured above, use the URL: `http://<server>/podcast/TheAwesomePodcast`

(where `TheAwesomePodcast` refers to the name in the JSON configuration file)

Use at you own risk!

## Docker Image

You can build a simple docker image using the provided Dockerfile by executing `docker build -t podcast-replay`. 

On your server, you can create a `config` directory and place a `podcast-replay.json` inside. Then you can run the service by running:

```bash
docker run -v "/path/to/config/:/code/config" podcast-replay:latest
```

This will start the service running at port 8088.
