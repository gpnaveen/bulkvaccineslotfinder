import requests
from datetime import date, timedelta
from multiprocessing import Pool

v_type = 'COVAXIN'
age = 18
districs = {
    264: 'Belgaum',
    265: 'BangaloreUrban',
    267: 'Gulbarga',
    270: 'Bagalkot',
    272: 'Bidar',
    278: 'Dharwad',
    293: 'Vijayapura',
    294: 'BBMP',
    371: 'Kolhapur',
    373: 'Sangli',
    375: 'Solapur',
}

today = date.today()
number_of_days_from_today = 1
center_list = []
store_details = {1: []}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) \
    Gecko/20100101 Firefox/87.0'}


# state ids 16 - KA , 21 - MH, 32 - Telangana
def get_slot_details(distr):
    global center_list
    counter = 1
    for dn in range(0, number_of_days_from_today):
        dt = (today + timedelta(days=dn)).strftime("%d-%m-%Y")
        dist_URL = \
            'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={0}&date={1}'.format(distr, dt)
        x_dist = requests.get(dist_URL, headers=headers)
        data = x_dist.json()
        vaccinefor18 = []
        for d in data["sessions"]:
            if d["min_age_limit"] == age and d['vaccine'] == v_type:
                centre_addr = "{3} Centre {0}:{1}:{2}".format(
                    counter, d['state_name'], d['district_name'], dt) + \
                    "\nCentre Adrress: " + d['name'] + \
                    "\nAvailable Capacity dose 1: " + str(
                    d["available_capacity_dose1"]) + \
                    "\nFees: " + str(d["fee"]) + "\n" + "\n"
                if d["available_capacity_dose1"] > 0:
                    vaccinefor18.append(centre_addr)
                    centre_addr = ''
                    counter = counter+1

        if(len(vaccinefor18) > 0):
            for i in vaccinefor18:
                center_list.append(i)
    return center_list


def run_parallel():
    pool = Pool(processes=len(districs.keys()))
    store_details[1] = pool.map(get_slot_details, districs.keys())
    pool.close()
    pool.join()
    for i, j in enumerate(store_details[1]):
        if j:
            print(i, ":", *j)


if __name__ == '__main__':
    run_parallel()
