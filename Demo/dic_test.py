def get_data():
    dat_others = [{'agent_host_ip': '10.69.184.12', 'agent_group': 'pc#10_69_184_12', 'provider_name': 's11_web'},
                  {'agent_host_ip': '10.69.184.39', 'agent_group': 'pc#10_69_184_39', 'provider_name': 's33_web'}]
    ip_list_data = {'10.69.184.12': [59389, '100%'], '10.69.184.39': [33333, '333%']}
    task_error = []
    for job in dat_others:
        if job["agent_group"] == "":
            agent_group = "null"
        else:
            agent_group = job["agent_group"]
        if job["provider_name"] == "":
            provider_name = "null"
        else:
            provider_name = job["provider_name"]
        ip_provider_names = [{"ip": job["agent_host_ip"], "agent_group": agent_group, "provider_name": provider_name}]
        #print("ip_provider_names: " + str(ip_provider_names))
        ip_provider_data = [key for item in ip_provider_names for key in item.values()]
        #print("ip_provider_data:" + str(ip_provider_data))
        for key in ip_list_data:
            if key == ip_provider_data[0]:
                ip_list_data[key].append(ip_provider_data[1])
                ip_list_data[key].append(ip_provider_data[2])
        print(ip_list_data)
        for ip_res in ip_list_data.items():
            res = f"{ip_res[1][1]} failed:http://{ip_res[0]}:8000/data/log/uat/{ip_res[1][0]}.txt "

        task_error.append((ip_provider_data[1], ip_provider_data[2], res))

    print("——task_error" + str(task_error))


if __name__ == '__main__':
    get_data()
