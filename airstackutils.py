import asyncio
from airstack.execute_query import AirstackClient
import os, json

async def get_all_pages(api_client, query, variables, typ):
    execute_query_client = api_client.create_execute_query_object(query=query, variables=variables)
    query_response = await execute_query_client.execute_paginated_query()
    if query_response.status_code == 200:
        data = query_response.data
        if typ in ['scrfollowing', 'scrfollower']:
            fid_dict = parse_social_data(data, typ)
        elif typ in ['followers', 'following']:
            fid_list = parse_fids(data, typ)
        while query_response.has_next_page:
            next_page_response = await query_response.get_next_page
            if next_page_response.status_code == 200:
                next_data = next_page_response.data
                if typ in ['scrfollowing', 'scrfollower']:
                    next_fid_dict = parse_social_data(next_data, typ)
                    fid_dict.update(next_fid_dict)
                elif typ in ['followers', 'following']:
                    next_fid_list = parse_fids(next_data, typ)
                    fid_list.extend(next_fid_list)
            else:
                break
            query_response = next_page_response
        if typ in ['scrfollowing', 'scrfollower']:
            return fid_dict
        elif typ in ['followers', 'following']:
            return fid_list
    else:
        print(query_response.error)
        return {}

async def getFollowingFIDWithSCR(api_client, fid):
    query = """query GetSocialFollowingsBySocialCapitalRank {
     SocialFollowings(
      input: {filter: {dappName: {_eq: farcaster}, identity: {_eq: "fc_fid:%s"}}, blockchain: ALL}
     ) {
      Following {
       followingProfileId
       followingAddress {
        socials {
         socialCapital {
          socialCapitalRank
         }
         profileHandle
        }
       }
      }
     }
    }"""%(fid)
    variables = {}
    fid_dict = await get_all_pages(api_client, query, variables, typ='scrfollowing')
    # sort fid_dict by value
    fid_dict = dict(sorted(fid_dict.items(), key=lambda item: item[1], reverse=False))
    return fid_dict

async def getFollowersFIDWithSCR(api_client, fid):
    query = """query GetSocialFollowersBySocialCapitalRank {
     SocialFollowers(
      input: {filter: {dappName: {_eq: farcaster}, identity: {_eq: "fc_fid:%s"}}, blockchain: ALL}
     ) {
      Follower {
       followerProfileId
       followerAddress {
        socials {
         socialCapital {
          socialCapitalRank
         }
         profileHandle
        }
       }
      }
     }
    }"""%(fid)
    variables = {}
    fid_dict = await get_all_pages(api_client, query, variables, typ='scrfollower')
    # sort fid_dict by value
    fid_dict = dict(sorted(fid_dict.items(), key=lambda item: item[1], reverse=False))
    return fid_dict

async def getFollowersAsList(api_client, fid):
    query = """query GetFollowersByFid {
        SocialFollowers(
            input: {filter: {identity: {_eq: "fc_fid:%s"}}, blockchain: ALL, limit: 100}
        ) {
            Follower {
            followerProfileId
            followerAddress {
                socials {
                profileHandle
                }
            }
            }
        }
        }"""%(fid)
    variables = {}
    fids = await get_all_pages(api_client, query, variables, typ='followers')
    return fids

async def getFollowingAsList(api_client, fid):
    query = """query GetFollowingByFid {
        SocialFollowings(
            input: {filter: {identity: {_eq: "fc_fid:%s"}}, blockchain: ALL, limit: 100}
        ) {
            Following {
            followingProfileId
            followingAddress {
                socials {
                profileHandle
                }
            }
            }
        }
        }"""%(fid)
    variables = {}
    fids = await get_all_pages(api_client, query, variables, typ='following')
    return fids

def parse_social_data(data, typ):
    if typ == 'scrfollowing':
        sTags = ['SocialFollowings', 'Following', 'followingProfileId', 'followingAddress']
    elif typ == 'scrfollower':
        sTags = ['SocialFollowers', 'Follower', 'followerProfileId', 'followerAddress']
    else:
        return None
    result = {}
    for following in data[sTags[0]][sTags[1]]:
        profile_id = following[sTags[2]]
        socials = following[sTags[3]]['socials']
        
        max_social_capital_rank = max((s['socialCapital']['socialCapitalRank'] for s in socials), default=0)
        max_social_capital_rank_handle = next((s['profileHandle'] for s in socials if s['socialCapital']['socialCapitalRank'] == max_social_capital_rank), None)

        result[profile_id] = [max_social_capital_rank, max_social_capital_rank_handle]
    return result

def parse_fids(data, typ):
    if typ == 'following':
        sTags = ['SocialFollowings', 'Following', 'followingProfileId', 'followingAddress']
    elif typ == 'followers':
        sTags = ['SocialFollowers', 'Follower', 'followerProfileId', 'followerAddress']
    else:
        return None
    result = []
    for following in data[sTags[0]][sTags[1]]:
        profile_id = following[sTags[2]]
        result.append(profile_id)
    return result

def get_Fname_from_fid(fid):
    fname = ""
    return fname

async def main():
    api_client = AirstackClient(api_key=os.getenv("AIRSTACK_API_KEY"))

    fid = '6846'
    lim = 10
    #await getFollowingFIDWithSCR(api_client, fid)
    #await getFollowersFIDWithSCR(api_client, fid)
    #await getFollowersAsList(api_client, fid)
    #await getFollowingAsList(api_client, fid)

    #get all followers with SCR, sort them by SCR
    #go through ascending order of SCR and see if fid follows them back.
    #if not, add to a list and once the list size reaches limit, return the list

    followers_with_scr = await getFollowersFIDWithSCR(api_client, fid)
    following_fids = await getFollowingAsList(api_client, fid)

    cnt = 0
    for item in followers_with_scr.keys():
        if item not in following_fids:
            print('SCR: %s, fid: %s , URL: %s'%(followers_with_scr[item][0], item, 'https://warpcast.com/'+followers_with_scr[item][1]))
            cnt+=1
            if cnt == lim:
                break
    return True

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

