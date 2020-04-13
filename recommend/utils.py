from blog.models import Vote
import csv
import pandas as pd


def create_dataset(users, blogs):
    mainlis = []
    for blog in blogs:
        bpk = blog.pk
        cpk = blog.community.pk
        lis = [bpk, cpk]
        for user in users:
            if Vote.objects.filter(blog=blog, user=user):
                lis.append(1)
            else:
                lis.append(0)
        mainlis.append(lis)
    my_df = pd.DataFrame(mainlis)
    my_df.to_csv('recommendation_dataset.csv', index=False, header=False)
    # with open("recommend_dataset.csv", "w", newline="") as f:
    #     writer = csv.writer(f)
    #     writer.writerows(mainlis)
