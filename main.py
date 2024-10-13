import requests
import networkx as nx
import matplotlib.pyplot as plt

# Ваш токен доступа и версия API
ACCESS_TOKEN = 'c79b0b65c79b0b65c79b0b659dc7e36f1ccc79bc79b0b65a743cc491d40249cc9a9b76a'
VERSION = '5.131'

# Имена пользователей VK, для которых будем собирать информацию
usernames = ['gogo_where_i_go', 'lazyl3ones', 'stuntlove']

# Ограничение на количество друзей
FRIENDS_LIMIT = 100

# Функция для получения ID пользователей по их никнеймам
def get_user_ids(usernames):
    url = f"https://api.vk.com/method/users.get?user_ids={','.join(usernames)}&access_token={ACCESS_TOKEN}&v={VERSION}"
    response = requests.get(url)
    data = response.json()
    
    # Проверка на наличие ошибок
    if 'error' in data:
        print("Ошибка в запросе:", data['error']['error_msg'])
        return {}
    
    # Возвращаем ID пользователей и их имена
    return {user['id']: f"{user['first_name']} {user['last_name']}" for user in data.get('response', [])}

# Функция для получения списка друзей (ограничим количеством)
def get_friends(user_id):
    url = f"https://api.vk.com/method/friends.get?user_id={user_id}&count={FRIENDS_LIMIT}&access_token={ACCESS_TOKEN}&v={VERSION}"
    response = requests.get(url)
    data = response.json()

    # Проверка на наличие ошибок
    if 'error' in data:
        print(f"Ошибка при получении друзей для пользователя {user_id}: {data['error']['error_msg']}")
        return []
    
    return data.get('response', {}).get('items', [])

# Шаг 1: Получаем ID пользователей
user_ids = get_user_ids(usernames)
if not user_ids:
    print("Не удалось получить ID пользователей. Проверьте запросы.")
else:
    print("User IDs:", user_ids)

    # Шаг 2: Получаем списки друзей (только первая степень, ограничение на количество)
    friends_data = {}
    
    for user_id in user_ids:
        friends = get_friends(user_id)
        friends_data[user_id] = friends
        print(f"Friends of {user_ids[user_id]} (ID {user_id}): {friends}")
    
    # Шаг 3: Создаем граф друзей
    G = nx.Graph()

    # Добавляем рёбра для каждого пользователя и его друзей
    for user_id, friends in friends_data.items():
        for friend in friends:
            G.add_edge(user_ids.get(user_id, user_id), friend)

    if len(G.edges()) > 0:
        # Шаг 4: Оценка центральностей

        # Центральность собственного вектора (eigenvector centrality)
        eigenvector = nx.eigenvector_centrality(G)

        # Центральность по близости (closeness centrality)
        closeness = nx.closeness_centrality(G)

        # Центральность по посредничеству (betweenness centrality)
        betweenness = nx.betweenness_centrality(G)

        # Оставляем только участников вашей группы для оценки
        group_members = {user_ids[user_id] for user_id in user_ids}

        group_eigenvector = {node: eigenvector[node] for node in group_members}
        group_closeness = {node: closeness[node] for node in group_members}
        group_betweenness = {node: betweenness[node] for node in group_members}

        # Шаг 5: Визуализация графа
        plt.figure(figsize=(12, 10))

        # Настраиваем цвета и размеры узлов в зависимости от центральностей
        node_colors = [eigenvector.get(node, 0.1) for node in G.nodes()]
        node_sizes = [2000 * closeness.get(node, 0.1) for node in G.nodes()]

        # Визуализация графа с красивыми цветами и стилями
        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, with_labels=False, node_color=node_colors, node_size=node_sizes,
                cmap=plt.cm.RdYlBu, edge_color="gray", alpha=0.7)

        # Подписываем только ключевые узлы (основные участники группы)
        labels = {node: node for node in group_members}
        nx.draw_networkx_labels(G, pos, labels, font_size=12, font_weight='bold', font_color='black')

        plt.title("Sample Graph Output With Centralities")
        plt.show()
        
        # Вывод результатов центральностей
        print("Eigenvector Centrality for Group Members:", group_eigenvector)
        print("Closeness Centrality for Group Members:", group_closeness)
        print("Betweenness Centrality for Group Members:", group_betweenness)

    else:
        print("Граф пустой, нет данных для оценки центральностей.")
