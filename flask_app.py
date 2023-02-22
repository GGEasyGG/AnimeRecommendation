from flask import Flask, render_template, request
import pandas as pd
import pickle
from sklearn.neighbors import NearestNeighbors


dataset = pd.read_csv('dataset.csv', index_col='anime_id')
file_name = "model_knn.pkl"
model_knn = pickle.load(open(file_name, "rb"))
df_anime = pd.read_csv('anime.csv')

lst = list(df_anime[df_anime['anime_id'].isin(dataset.index)]['name'])

app = Flask(__name__)


def get_url(name):
    query = name.replace(' ', '+')
    url = f"https://google.com/search?q={query}"
    return url


@app.route('/', methods=['GET', 'POST'])
def compute():
  if request.method == "GET":
      return render_template('get.html', lst=lst)
  elif request.method == "POST":
        anime_name = request.form['lst']
        anime_id = int(df_anime[df_anime['name'] == anime_name]['anime_id'])
        distances, indices = model_knn.kneighbors(dataset[dataset.index == anime_id].values.reshape(1, -1), n_neighbors=11)
        rec_list = []
        for i in range(1, len(distances.flatten())):
            rec_list.append(df_anime[df_anime['anime_id'] == dataset.index[indices.flatten()[i]]]['name'].values[0])

        res = pd.DataFrame(pd.Series(rec_list))

        res["Press to search in Google"] = res[0].apply(lambda x: f"<a href='{get_url(x)}'>{x}</a>")
        res.index += 1
        res = res.rename(columns={0: 'Recommended anime'})
        return render_template('post.html', tables=[res.to_html(render_links=True, escape=False, classes='data', header="true", justify='center')], title="Recommendation for anime \"" + df_anime[df_anime['anime_id'] == anime_id]['name'].values[0] + "\"", site=f"<a href='{get_url(df_anime[df_anime['anime_id'] == anime_id]['name'].values[0])}'>{df_anime[df_anime['anime_id'] == anime_id]['name'].values[0]}</a>")


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8000)
