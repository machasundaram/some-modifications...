import requests
import json
import re
import base64
import pyperclip
from pywidevine.L3.cdm import cdm, deviceconfig
from base64 import b64encode
from pywidevine.L3.getPSSH import get_pssh
from pywidevine.L3.decrypt.wvdecryptcustom import WvDecrypt
import subprocess
from pathlib import Path
import os
import winsound
import ctypes

ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 6 )

# Define the function to process a single URL
def process_url(url):
    
    api_url = "https://spapi.zee5.com/singlePlayback/getDetails/secure"

    # Define common JSON data and headers
    data = {
        "x-access-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwbGF0Zm9ybV9jb2RlIjoiV2ViQCQhdDM4NzEyIiwiaXNzdWVkQXQiOiIyMDIzLTA5LTMwVDA2OjMwOjM0LjMwNloiLCJwcm9kdWN0X2NvZGUiOiJ6ZWU1QDk3NSIsInR0bCI6ODY0MDAwMDAsImlhdCI6MTY5NjA1NTQzNH0.fRBzqRIAsDDZqmJQFT2l3zkFxTYtYN5jXgAIoLYh0oo",
        "Authorization": "bearer eyJraWQiOiJlNmxfbGYweHpwYVk4VzBNcFQzWlBzN2hyOEZ4Y0trbDhDV0JaekVKT2lBIiwidHlwIjoiSldUIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiI3NTk4NkU2MS00NERELTRCOUUtQkI5MS1EMzg3MDI4QzYyODgiLCJzdWJzY3JpcHRpb25zIjoiW10iLCJhY3RpdmF0aW9uX2RhdGUiOiIyMDIxLTEyLTAzVDA4OjAxOjAzLjQxN1oiLCJhbXIiOlsiZGVsZWdhdGlvbiJdLCJpc3MiOiJodHRwczovL3VzZXJhcGkuemVlNS5jb20iLCJjdXJyZW50X2NvdW50cnkiOiJJTiIsImNsaWVudF9pZCI6InJlZnJlc2hfdG9rZW5fY2xpZW50IiwiYWNjZXNzX3Rva2VuX3R5cGUiOiJEZWZhdWx0UHJpdmlsZWdlIiwidXNlcl90eXBlIjoiUmVnaXN0ZXJlZCIsInNjb3BlIjpbInVzZXJhcGkiLCJzdWJzY3JpcHRpb25hcGkiLCJwcm9maWxlYXBpIl0sImF1dGhfdGltZSI6MTY5MDYwNjUwOSwiZXhwIjoxNjk2NTk5MTU3LCJpYXQiOjE2OTM5NjkxNTcsInVzZXJfZW1haWwiOiJzd2FwbmlsdXBhZGh5YXlrcmF0b3NAZ21haWwuY29tIiwiZGV2aWNlX2lkIjoiNmMwZDVlMjAtZTdiYi00MWFkLTg0NDItODUxOWIwZmFkYThhIiwicmVnaXN0cmF0aW9uX2NvdW50cnkiOiJJTiIsInZlcnNpb24iOjQsImF1ZCI6WyJ1c2VyYXBpIiwic3Vic2NyaXB0aW9uYXBpIiwicHJvZmlsZWFwaSJdLCJzeXN0ZW0iOiJaNSIsIm5iZiI6MTY5Mzk2OTE1NywiaWRwIjoibG9jYWwiLCJ1c2VyX2lkIjoiNzU5ODZlNjEtNDRkZC00YjllLWJiOTEtZDM4NzAyOGM2Mjg4IiwiY3JlYXRlZF9kYXRlIjoiMjAyMS0xMi0wM1QwODowMTowMy40MTdaIiwiYWN0aXZhdGVkIjp0cnVlfQ.hNDQXPvX13EuYonEnIEkqrSuu-XEoI6miaINpCK-kQ0s1_BIyuELfOi4ZzzYYRpqXoAD-A9-EbHB5L8cumPDIQsH6gSkZ_1Rd1gOyDN8SHDguJXdEbIdn7K87F3KXmC_TaVAfWEFAw3AkHggEPoePQ0u5w8i6Ljj7EGfyqOYY4aoaamdRkb1Erk-9hFwGY3yDXsXwxXNF4su1sK-1v1rEGBNieqvjhzBXqTT7PoLTsrFIZrevMi3opN41l_pQMEscIKr0qZ9osq_qpUG8mJAmzhYpDutAYbdrufqMSMU2CEZX-tSQI0SzokCjvAvN0n2pp8aFpFLqt-kmYtk93VRrw",
        "x-dd-token": "eyJzY2hlbWFfdmVyc2lvbiI6IjEiLCJvc19uYW1lIjoiTi9BIiwib3NfdmVyc2lvbiI6Ik4vQSIsInBsYXRmb3JtX25hbWUiOiJDaHJvbWUiLCJwbGF0Zm9ybV92ZXJzaW9uIjoiMTA0IiwiZGV2aWNlX25hbWUiOiIiLCJhcHBfbmFtZSI6IldlYiIsImFwcF92ZXJzaW9uIjoiMi41Mi4zMSIsInBsYXllcl9jYXBhYmlsaXRpZXMiOnsiYXVkaW9fY2hhbm5lbCI6WyJTVEVSRU8iXSwidmlkZW9fY29kZWMiOlsiSDI2NCJdLCJjb250YWluZXIiOlsiTVA0IiwiVFMiXSwicGFja2FnZSI6WyJEQVNIIiwiSExTIl0sInJlc29sdXRpb24iOlsiMjQwcCIsIlNEIiwiSEQiLCJGSEQiXSwiZHluYW1pY19yYW5nZSI6WyJTRFIiXX0sInNlY3VyaXR5X2NhcGFiaWxpdGllcyI6eyJlbmNyeXB0aW9uIjpbIldJREVWSU5FX0FFU19DVFIiXSwid2lkZXZpbmVfc2VjdXJpdHlfbGV2ZWwiOlsiTDMiXSwiaGRjcF92ZXJzaW9uIjpbIkhEQ1BfVjEiLCJIRENQX1YyIiwiSERDUF9WMl8xIiwiSERDUF9WMl8yIl19fQ=="}

    m3u8DL_RE = 'N_m3u8DL-RE'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/116.0',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/json',
        'Referer': 'https://www.zee5.com/',
        'Origin': 'https://www.zee5.com',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }

    url = urls
    # Split the URL by '/' and get the relevant parts
    url_parts = url.split('/')

    # Extract the content_id and show_id from the URL
    content_id = url_parts[-1]  # Last part of the URL
    show_id = url_parts[-3]  # Second-to-last part of the URL

    # Define the payload data for this URL
    payload = {
        "content_id": content_id,
        "show_id": show_id,
        "device_id": "6c0d5e20-e7bb-41ad-8442-8519b0fada8a",
        "platform_name": "desktop_web",
        "translation": "en",
        "user_language": "en,hi,hr",
        "country": "IN",
        "state": "UT",
        "app_version": "3.13.0",
        "user_type": "register",
        "check_parental_control": "false",
        "gender": "Unknown",
        "uid": "75986e61-44dd-4b9e-bb91-d387028c6288",
        "ppid": "6c0d5e20-e7bb-41ad-8442-8519b0fada8a",
        "version": "12"
    }

    # Convert the JSON data dictionary to JSON format
    json_data = json.dumps(data)

    # Make the POST request with JSON data, payload, and headers for this URL
    response = requests.post(api_url, data=json_data, headers=headers, params=payload)

    # Check the response for this URL
    if response.status_code == 200:
        # Request was successful
        try:
            # Parse the JSON response
            response_data = response.json()
            key_os_details = response_data.get("keyOsDetails", {})
            nl_data = key_os_details.get("nl")
            sdrm_data = key_os_details.get("sdrm")

            
            
        except json.JSONDecodeError:
            print(f"Failed to parse JSON response for URL '{url}'")

    # Split the URL by '/' and get the relevant parts
    url_parts = url.split('/')

    # Extract the content_id and show_id from the URL
    content_id = url_parts[-1]
    url = "https://gwapi.zee5.com/content/details/" + content_id + "?translation=en&country=IN&version=2"
    headers = {
        "x-access-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwbGF0Zm9ybV9jb2RlIjoiV2ViQCQhdDM4NzEyIiwiaXNzdWVkQXQiOiIyMDIzLTA5LTAxVDIyOjI5OjEwLjgzOVoiLCJwcm9kdWN0X2NvZGUiOiJ6ZWU1QDk3NSIsInR0bCI6ODY0MDAwMDAsImlhdCI6MTY5MzYwNzM1MH0.YZqrXyr5Uqm3g5fzCTbCJbzRynWnEaJWSUpmJWKRsyM"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception if the response status code is not 200 (OK)

        data = response.json()  # Parse the JSON response

        # Check if the "video_details" field is present in the JSON data
        if "video_details" in data:
            video_details = data["video_details"]

            # Check if the "url" field is present in the video_details
            if "url" in video_details:
                url = video_details["url"]

                # Prepend the URL with the specified prefix
                mediacloudfront_url = "https://mediacloudfront.zee5.com" + url
                print("Media Cloudfront URL:", mediacloudfront_url)

                # Download the MPD manifest
                mpd_response = requests.get(mediacloudfront_url)
                mpd_response.raise_for_status()

                # Search for PSSH within <cenc:pssh> tags using regex
                pssh_matches = re.findall(r'<cenc:pssh>(.*?)</cenc:pssh>', mpd_response.text, re.DOTALL)

                if pssh_matches:
                    shortest_pssh = min(pssh_matches, key=len)
                    print("Shortest PSSH found in the MPD:")
                    print(shortest_pssh)
                else:
                    print("PSSH not found in the MPD.")
            else:
                print("The 'url' field is not present in the video_details.")
        else:
            print("The 'video_details' field is not present in the JSON response.")

    except requests.exceptions.RequestException as e:
        print("Error making the GET request:", e)

    except ValueError as e:
        print("Error parsing JSON response:", e)

    # Define your headers here
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/116.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/octet-stream',
        'Referer': 'https://www.zee5.com/',
        'nl': nl_data,
        'customdata': sdrm_data,
        'Origin': 'https://www.zee5.com',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }

    pssh = shortest_pssh
    lic_url = 'https://spapi.zee5.com/widevine/getLicense'

    def WV_Function(pssh, lic_url, cert_b64=None):
        wvdecrypt = WvDecrypt(init_data_b64=pssh, cert_data_b64=cert_b64, device=deviceconfig.device_android_generic)
        widevine_license = requests.post(url=lic_url, data=wvdecrypt.get_challenge(), headers=headers)
        license_b64 = b64encode(widevine_license.content)
        wvdecrypt.update_license(license_b64)
        Correct, keyswvdecrypt = wvdecrypt.start_process()
        if Correct:
            return Correct, keyswvdecrypt

    correct, keys = WV_Function(pssh, lic_url)

    print()
    for key in keys:
        ke_ys = ' '.join([f'--key {key}' for key in keys]).split()
        print('--key ' + key)
        

        # Build the key_string to make all keys easily copyable
        key_string = ' '.join([f"--key {key}" for key in keys])
        
        

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/117.0',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/json',
            'Referer': 'https://www.zee5.com/',
            'Origin': 'https://www.zee5.com',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }

        json_data = {
            "x-access-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwbGF0Zm9ybV9jb2RlIjoiV2ViQCQhdDM4NzEyIiwiaXNzdWVkQXQiOiIyMDIzLTA5LTMwVDA2OjMwOjM0LjMwNloiLCJwcm9kdWN0X2NvZGUiOiJ6ZWU1QDk3NSIsInR0bCI6ODY0MDAwMDAsImlhdCI6MTY5NjA1NTQzNH0.fRBzqRIAsDDZqmJQFT2l3zkFxTYtYN5jXgAIoLYh0oo",
            "Authorization": "bearer eyJraWQiOiJlNmxfbGYweHpwYVk4VzBNcFQzWlBzN2hyOEZ4Y0trbDhDV0JaekVKT2lBIiwidHlwIjoiSldUIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiI3NTk4NkU2MS00NERELTRCOUUtQkI5MS1EMzg3MDI4QzYyODgiLCJzdWJzY3JpcHRpb25zIjoiW10iLCJhY3RpdmF0aW9uX2RhdGUiOiIyMDIxLTEyLTAzVDA4OjAxOjAzLjQxN1oiLCJhbXIiOlsiZGVsZWdhdGlvbiJdLCJpc3MiOiJodHRwczovL3VzZXJhcGkuemVlNS5jb20iLCJjdXJyZW50X2NvdW50cnkiOiJJTiIsImNsaWVudF9pZCI6InJlZnJlc2hfdG9rZW5fY2xpZW50IiwiYWNjZXNzX3Rva2VuX3R5cGUiOiJEZWZhdWx0UHJpdmlsZWdlIiwidXNlcl90eXBlIjoiUmVnaXN0ZXJlZCIsInNjb3BlIjpbInVzZXJhcGkiLCJzdWJzY3JpcHRpb25hcGkiLCJwcm9maWxlYXBpIl0sImF1dGhfdGltZSI6MTY5MDYwNjUwOSwiZXhwIjoxNjk2NTk5MTU3LCJpYXQiOjE2OTM5NjkxNTcsInVzZXJfZW1haWwiOiJzd2FwbmlsdXBhZGh5YXlrcmF0b3NAZ21haWwuY29tIiwiZGV2aWNlX2lkIjoiNmMwZDVlMjAtZTdiYi00MWFkLTg0NDItODUxOWIwZmFkYThhIiwicmVnaXN0cmF0aW9uX2NvdW50cnkiOiJJTiIsInZlcnNpb24iOjQsImF1ZCI6WyJ1c2VyYXBpIiwic3Vic2NyaXB0aW9uYXBpIiwicHJvZmlsZWFwaSJdLCJzeXN0ZW0iOiJaNSIsIm5iZiI6MTY5Mzk2OTE1NywiaWRwIjoibG9jYWwiLCJ1c2VyX2lkIjoiNzU5ODZlNjEtNDRkZC00YjllLWJiOTEtZDM4NzAyOGM2Mjg4IiwiY3JlYXRlZF9kYXRlIjoiMjAyMS0xMi0wM1QwODowMTowMy40MTdaIiwiYWN0aXZhdGVkIjp0cnVlfQ.hNDQXPvX13EuYonEnIEkqrSuu-XEoI6miaINpCK-kQ0s1_BIyuELfOi4ZzzYYRpqXoAD-A9-EbHB5L8cumPDIQsH6gSkZ_1Rd1gOyDN8SHDguJXdEbIdn7K87F3KXmC_TaVAfWEFAw3AkHggEPoePQ0u5w8i6Ljj7EGfyqOYY4aoaamdRkb1Erk-9hFwGY3yDXsXwxXNF4su1sK-1v1rEGBNieqvjhzBXqTT7PoLTsrFIZrevMi3opN41l_pQMEscIKr0qZ9osq_qpUG8mJAmzhYpDutAYbdrufqMSMU2CEZX-tSQI0SzokCjvAvN0n2pp8aFpFLqt-kmYtk93VRrw",
            "x-dd-token": "eyJzY2hlbWFfdmVyc2lvbiI6IjEiLCJvc19uYW1lIjoiTi9BIiwib3NfdmVyc2lvbiI6Ik4vQSIsInBsYXRmb3JtX25hbWUiOiJDaHJvbWUiLCJwbGF0Zm9ybV92ZXJzaW9uIjoiMTA0IiwiZGV2aWNlX25hbWUiOiIiLCJhcHBfbmFtZSI6IldlYiIsImFwcF92ZXJzaW9uIjoiMi41Mi4zMSIsInBsYXllcl9jYXBhYmlsaXRpZXMiOnsiYXVkaW9fY2hhbm5lbCI6WyJTVEVSRU8iXSwidmlkZW9fY29kZWMiOlsiSDI2NCJdLCJjb250YWluZXIiOlsiTVA0IiwiVFMiXSwicGFja2FnZSI6WyJEQVNIIiwiSExTIl0sInJlc29sdXRpb24iOlsiMjQwcCIsIlNEIiwiSEQiLCJGSEQiXSwiZHluYW1pY19yYW5nZSI6WyJTRFIiXX0sInNlY3VyaXR5X2NhcGFiaWxpdGllcyI6eyJlbmNyeXB0aW9uIjpbIldJREVWSU5FX0FFU19DVFIiXSwid2lkZXZpbmVfc2VjdXJpdHlfbGV2ZWwiOlsiTDMiXSwiaGRjcF92ZXJzaW9uIjpbIkhEQ1BfVjEiLCJIRENQX1YyIiwiSERDUF9WMl8xIiwiSERDUF9WMl8yIl19fQ=="}
        response = requests.post(
            api_url + "?content_id=" + content_id + "&show_id=" + show_id + "&device_id=6c0d5e20-e7bb-41ad-8442-8519b0fada8a&platform_name=desktop_web&translation=en&user_language=en,hi,hr&country=IN&state=UP&app_version=3.14.4&user_type=register&check_parental_control=false&uid=75986e61-44dd-4b9e-bb91-d387028c6288&ppid=6c0d5e20-e7bb-41ad-8442-8519b0fada8a&version=12",
            headers=headers,
            json=json_data,
        )

        # Parse the JSON response
        data = response.json()

        if 'assetDetails' in data:
            # Access the 'video_url' dictionary within 'assetDetails'
            video_url = data['assetDetails'].get('video_url', {})

            # Access the 'mpd' value within 'video_url'
            old_mpd_url = video_url.get('mpd', None)

            if old_mpd_url is not None:
                print("MPD Value:", old_mpd_url)

            else:
                print("'mpd' not found in 'video_url'")
        else:
            print("'assetDetails' not found in JSON response")

        
        subprocess.run(['yt-dlp', '-k', '--allow-unplayable-formats', '--no-check-certificate', '-N', '8', '-f', 'wv*[height=144]/wv*[height=240]/wv*[height=360]', '--fixup', 'never', old_mpd_url, '-o', 'encrypted.mp4'])
        subprocess.run(['mp4decrypt' ,'--key', key, 'encrypted.mp4', 'decrypted.mp4'], shell=True)
        subprocess.call([r'G:\Experiment\1process\zee\Thumb.bat'])
        
        print("Cleaning Directory...")
        os.remove("encrypted.mp4")
        os.remove("decrypted.mp4")
        duration = 500
        freq = 1800
        winsound.Beep(freq, duration)
        

urls = pyperclip.paste()

for url in urls:
    process_url(url)
    exit()