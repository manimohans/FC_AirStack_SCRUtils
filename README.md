# Farcaster User Discovery using Social Capital Rank

This Python script utilizes the Airstack API to analyze Farcaster users' social connections based on their Social Capital Rank (SCR). It can identify high-ranking followers who aren't being followed back, potentially revealing influential users to engage with.

## Features

* **Get followers/following with SCR:** Retrieves a user's followers or following list, sorted by their Social Capital Rank.
* **Identify unreciprocated followers:** Finds followers with high SCR who the user doesn't follow back.
* **Paginated API calls:** Handles paginated responses from the Airstack API to retrieve all results.
* **Programmable DC notification:** You can program it to send DC every N-number of days (or hours or months) - the same string.

## Prerequisites

* **Airstack Account:** Sign up for an account at [https://airstack.xyz/](https://airstack.xyz/) and obtain your API key.
* **Python Environment:** Ensure you have Python 3.x installed.
* **Required Libraries:** 
   - `airstack` (Install using `pip3 install airstack`)

## Setup

1. **Install dependencies:** Run `pip3 install airstack`
2. **Set API key:** 
   - Either set the `AIRSTACK_API_KEY` environment variable:
     ```bash
     export AIRSTACK_API_KEY=your_api_key
     ```
   - Or modify the `main` function to pass your API key directly:
     ```python
     api_client = AirstackClient(api_key="your_api_key") 
     ```

## Usage

1. **Modify the `fid` variable in the `main` function:**  
   - Replace `'6846'` with the Farcaster User ID (FID) you want to analyze.
2. **Run the script:**  
   - Execute `python airstackutils.py`
3. **Output:** 
   - The script will print up to 10 (default limit) followers with high SCR that the specified user doesn't follow back. 
   - Each line will display a list containing: SCR, FID, Warpcast URL (profileHandle that Airstack returns is confusing - need to test!)
     - Example output:  
      SCR: 12, fid: 576, URL: https://warpcast.com/username  
      SCR: 61, fid: 631, URL: https://warpcast.com/anotheruser
   

## Functions

- `get_all_pages(api_client, query, variables, typ)`: Fetches paginated results from the Airstack API based on the provided query and type (`scrfollowing`, `scrfollower`, `followers`, or `following`).
- `getFollowingFIDWithSCR(api_client, fid)`: Retrieves the following list of the user with their SCR, sorted in ascending order.
- `getFollowersFIDWithSCR(api_client, fid)`: Retrieves the followers of the user with their SCR, sorted in ascending order.
- `getFollowersAsList(api_client, fid)`: Retrieves the list of followers of the user.
- `getFollowingAsList(api_client, fid)`: Retrieves the list of users followed by the specified user.
- `parse_social_data(data, typ)`: Parses the Airstack API response to extract relevant data (SCR and profile handles for `scrfollowing` and `scrfollower`, or profile IDs for `followers` and `following`).
- `parse_fids(data, typ)`: Parses the Airstack API response to extract profile IDs for followers and following.
- `get_Fname_from_fid(fid)`: (Not implemented) Could be used to fetch the user's name from their FID.


Contact @mani (farcaster) for feature requests or help!
