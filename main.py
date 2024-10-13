import requests
import networkx as nx
import matplotlib.pyplot as plt

ACCESS_TOKEN = 'c79b0b65c79b0b65c79b0b659dc7e36f1ccc79bc79b0b65a743cc491d40249cc9a9b76a'
VERSION = '5.131'

usernames = ['gogo_where_i_go', 'lazyl3ones', 'stuntlove']

FRIENDS_LIMIT = 100

def get_user_ids(usernames):
    url = f"https://api.vk.com/method/users.get?user_ids={','.join(usernames)}&access_token={ACCESS_TOKEN}&v={VERSION}"
    response = requests.get(url)
    data = response.json()

    if 'error' in data:
        print("Ошибка в запросе:", data['error']['error_msg'])
        return {}

    return {user['id']: f"{user['first_name']} {user['last_name']}" for user in data.get('response', [])}

def get_friends(user_id):
    url = f"https://api.vk.com/method/friends.get?user_id={user_id}&count={FRIENDS_LIMIT}&access_token={ACCESS_TOKEN}&v={VERSION}"
    response = requests.get(url)
    data = response.json()

    if 'error' in data:
        print(f"Ошибка при получении друзей для пользователя {user_id}: {data['error']['error_msg']}")
        return []
    
    return data.get('response', {}).get('items', [])

user_ids = get_user_ids(usernames)
if not user_ids:
    print("Не удалось получить ID пользователей. Проверьте запросы.")
else:
    print("User IDs:", user_ids)

    friends_data = {}
    
    for user_id in user_ids:
        friends = get_friends(user_id)
        friends_data[user_id] = friends
        print(f"Friends of {user_ids[user_id]} (ID {user_id}): {friends}")

    G = nx.Graph()

    for user_id, friends in friends_data.items():
        for friend in friends:
            G.add_edge(user_ids.get(user_id, user_id), friend)

    if len(G.edges()) > 0:

        eigenvector = nx.eigenvector_centrality(G)

        closeness = nx.closeness_centrality(G)

        betweenness = nx.betweenness_centrality(G)

        group_members = {user_ids[user_id] for user_id in user_ids}

        group_eigenvector = {node: eigenvector[node] for node in group_members}
        group_closeness = {node: closeness[node] for node in group_members}
        group_betweenness = {node: betweenness[node] for node in group_members}

        plt.figure(figsize=(12, 10))

        node_colors = [group_eigenvector.get(node, 0.1) for node in G.nodes()]
        node_sizes = [2000 * group_closeness.get(node, 0.1) for node in G.nodes()]

        pos = nx.spring_layout(G, k=0.6, seed=42)
        nx.draw(G, pos, with_labels=False, node_color=node_colors, node_size=node_sizes,
                cmap=plt.cm.RdYlBu, edge_color="gray", alpha=0.7)

        labels = {node: node for node in group_members}
        nx.draw_networkx_labels(G, pos, labels, font_size=12, font_weight='bold', font_color='black')

        plt.title("Граф друзей (выделены члены группы)")
        plt.show()
        
        print("Eigenvector Centrality for Group Members:", group_eigenvector)
        print("Closeness Centrality for Group Members:", group_closeness)
        print("Betweenness Centrality for Group Members:", group_betweenness)

    else:
        print("Граф пустой, нет данных для оценки центральностей.")
