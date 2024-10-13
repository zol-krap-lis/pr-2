## Практика #2 Золотов А.А. Лисин С.В. Крапивин Я.С. (БСМО-11-24) 

# VK Friends Centrality Graph

Этот проект использует VK API для сбора информации о друзьях и их связях и строит граф с оценкой центральностей узлов (пользователей). Визуализация показывает структуру социальной сети, выделяя ключевых пользователей на основе различных показателей центральности.

## Описание

Код выполняет следующие шаги:

1. **Получение данных пользователей VK**: Идентифицирует пользователей по никнеймам, используя VK API.
2. **Сбор списка друзей**: Собирает список друзей для каждого пользователя.
3. **Построение графа**: Создаёт граф, где узлы — это пользователи, а рёбра — связи (дружба) между ними.
4. **Оценка центральностей**:
   - **Eigenvector Centrality**: Вычисляет влияние пользователя на основе его связей.
   - **Closeness Centrality**: Показывает, насколько близок пользователь ко всем остальным в сети.
   - **Betweenness Centrality**: Определяет, через каких пользователей проходят основные пути между другими пользователями.
5. **Визуализация графа**: Отображает граф с цветами узлов, которые зависят от их центральности.

## Установка

Для работы кода необходим Python с установленными библиотеками:

```bash
pip install requests networkx matplotlib

## Пример
![Пример](images/Снимок экрана 2024-10-13 223724.png)

