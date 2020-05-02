from blog.models import Vote, Comment
import csv
import pandas as pd
from utilities.recommend.knn_recommender import KnnRecommender


def create_dataset(users, blogs):
    mainlis = []
    for blog in blogs:
        bpk = blog.pk
        cpk = blog.community.pk
        comment_count = Comment.objects.filter(blog=blog).count()
        lis = [bpk, cpk, blog.view_count, blog.vote_count, comment_count]
        mainlis.append(lis)
    my_df = pd.DataFrame(mainlis)
    my_df = my_df.set_axis(['bpk', 'cpk', 'view_count', 'vote_count', 'comment_count'], axis='columns')
    my_df.to_csv('recommendation_dataset.csv', index=False)


def train_model():
    recommender = KnnRecommender('recommendation_dataset.csv')
    recommender.set_model_params()
    recommender.train()
    recommender.make_recommendations([[11, 4, 0, 0]])






# TODO - Idea dropped to be discussed later
# def create_dataset(users, blogs):
#     mainlis = []
#     for blog in blogs:
#         bpk = blog.pk
#         cpk = blog.community.pk
#         lis = [bpk, cpk]
#         for user in users:
#             if Vote.objects.filter(blog=blog, user=user):
#                 lis.append(1)
#             else:
#                 lis.append(0)
#         mainlis.append(lis)
#     my_df = pd.DataFrame(mainlis)
#     my_df.to_csv('recommendation_dataset.csv', index=False, header=False)
    # with open("recommend_dataset.csv", "w", newline="") as f:
    #     writer = csv.writer(f)
    #     writer.writerows(mainlis)
