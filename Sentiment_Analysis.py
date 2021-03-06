from textblob import TextBlob
from matplotlib import pyplot as plt
import pandas as pd


# This class does sentimental anaylsis on the tweets
class Analysis:
    # This method checks whether or not polarity and subjectivity
    def polarity_and_subjectivity(self):
        read = pd.read_csv("Voting.csv")  # reads in CSV file
        new_column = pd.DataFrame(read['text'])  # selects the text column and puts it into a data frame
        new_column.insert(0, 'name', read['name'])  # inserts column called name into the data frame
        new_column.insert(1, 'followers count', read['followers count']) # inserts column called followers count into the data frame
        new_column.insert(2, 'friends count', read['friends count']) # inserts column called followers count into the data frame
        new_column.insert(3, 'retweet count', read['retweet count'])  # inserts column called retweet count into data frame
        new_column.insert(4, 'favorite count', read['favorite count']) # inserts column called favorite count into data frame
        new_column['polarity'] = new_column.apply(lambda x: TextBlob(x['text']).sentiment.polarity,
                                                  axis=1)  # Inserts a new column by sentimental analysis of the text column
        new_column['subjectivity'] = new_column.apply(lambda x: TextBlob(x['text']).sentiment.subjectivity,
                                                      axis=1)  # Inserts a new column by sentimental analysis of the text column
        # separates range into 3 classes for polarity and subjectivity
        polarity_class0 = new_column['polarity'].between(-1.0, -0.2, inclusive=True)
        polarity_class1 = new_column['polarity'].between(-0.2, 0.2, inclusive=False)
        polarity_class2 = new_column['polarity'].between(0.2, 1.0, inclusive=True)
        subject_class0 = new_column['subjectivity'].between(0.0, 0.4, inclusive=True)
        subject_class1 = new_column['subjectivity'].between(0.4, 0.6, inclusive=False)
        subject_class2 = new_column['subjectivity'].between(0.6, 1.0, inclusive=True)
        new_column.insert(7, 'polarity between -1 to -0.2 (class 0)', polarity_class0)
        new_column.insert(8, 'polarity between -0.2 to 0.2 (class 1)', polarity_class1)
        new_column.insert(9, 'polarity between 0.2 to 1 (class 2)', polarity_class2)
        new_column.insert(11, 'subjectivity between 0 to 0.4 (class 0)',  subject_class0)
        new_column.insert(12, 'subjectivity between 0.4 to 0.6 (class 1)', subject_class1)
        new_column.insert(13, 'subjectivity between 0.6 to 1 (class 2)',  subject_class2)
        new_column.to_csv('Voting_sentiment_analysis.csv', index=False)  # puts the dataframe into a new csv file

    def scatter_plot(self):
        data = pd.read_csv("Voting_sentiment_analysis.csv")
        polarity = data['polarity']
        subjectivity = data['subjectivity']
        favorites = data['favorite count']
        plt.scatter(polarity, favorites, c=subjectivity, edgecolors='black', linewidths=0.5, alpha=5)
        cbar = plt.colorbar()
        cbar.set_label('Subjectivity')
        plt.xlabel('Polarity')
        plt.ylabel('Favorite Count')
        plt.grid(True)
        plt.tight_layout()
        plt.title('sentiment analysis with favorite and retweet count')
        plt.show()

    def line_plot(self):
        data = pd.read_csv("Voting_sentiment_analysis.csv")
        polarity = data['polarity']
        subjectivity = data['subjectivity']
        plt.scatter(subjectivity, polarity, edgecolors='black', linewidths=0.5)
        plt.xlabel('subjectivity')
        plt.ylabel('polarity')
        plt.title('polarity vs subjectivity')
        plt.show()

    def hist_plot(self):
        data = pd.read_csv("Voting_sentiment_analysis.csv")
        polarity = data['polarity']
        subjectivity = data['subjectivity']
        fig, axs = plt.subplots(1, 2, sharey=True)
        axs[0].hist(polarity, bins=10)
        axs[1].hist(subjectivity, bins=10)
        axs[0].set_title('Polarity Distribution')
        axs[0].set_xlabel('polarity')
        axs[0].set_ylabel('number of twitter users')
        axs[1].set_title('Subjectivity Distribution')
        axs[1].set_xlabel('subjectivity')
        plt.tight_layout()
        plt.show()

    def polarity_subjectivity_neutral(self):
        data = pd.read_csv("Voting_sentiment_analysis.csv",  dtype={'polarity between -0.2 to 0.2': str,'subjectivity between 0.4 to 0.6': str})
        df = pd.DataFrame(data)
        newdata = df[df['polarity between -0.2 to 0.2'].str.contains('True') & df['subjectivity between 0.4 to 0.6'].str.contains('True')]
        newdata.to_csv('Voting_polarity_and_subjectivity_neutral_range.csv', index=False)

    def subjectivity_class(self):
        data = pd.read_csv("Voting_sentiment_analysis.csv",  dtype={'subjectivity between 0 to 0.4 (class 0)': str, 'subjectivity between 0.4 to 0.6 (class 1)': str, 'subjectivity between 0.6 to 1 (class 2)': str})
        df = pd.DataFrame(data)
        df.loc[df['subjectivity between 0 to 0.4 (class 0)'].str.contains('True'), 'SubjectivityClass'] = '0'
        df.loc[df['subjectivity between 0.4 to 0.6 (class 1)'].str.contains('True'), 'SubjectivityClass'] = '1'
        df.loc[df['subjectivity between 0.6 to 1 (class 2)'].str.contains('True'), 'SubjectivityClass'] = '2'
        df.to_csv('Voting_sentiment_analysis.csv', index=False)

    def polarity_class(self):
        data = pd.read_csv("Voting_sentiment_analysis.csv",  dtype={'polarity between -1 to -0.2 (class 0)': str, 'polarity between -0.2 to 0.2 (class 1)': str, 'polarity between 0.2 to 1 (class 2)': str})
        df = pd.DataFrame(data)
        df.loc[df['polarity between -1 to -0.2 (class 0)'].str.contains('True'), 'PolarityClass'] = '0'
        df.loc[df['polarity between -0.2 to 0.2 (class 1)'].str.contains('True'), 'PolarityClass'] = '1'
        df.loc[df['polarity between 0.2 to 1 (class 2)'].str.contains('True'), 'PolarityClass'] = '2'
        df.to_csv('Voting_sentiment_analysis.csv', index=False)

    def to_subjectivity_classification(self):
        read = pd.read_csv("Voting_sentiment_analysis.csv")  # reads in CSV file
        new_column = pd.DataFrame()  # selects the text column and puts it into a data frame
        new_column.insert(0, 'followers count', read['followers count'])  # inserts column called followers count into the data frame
        new_column.insert(1, 'friends count', read['friends count'])  # inserts column called followers count into the data frame
        new_column.insert(2, 'retweet count', read['retweet count'])
        new_column.insert(3, 'favorite count', read['favorite count'])
        new_column.insert(4, 'polarity', read['polarity'])
        new_column.insert(5, 'SubjectivityClass', read['SubjectivityClass'])
        new_column.to_csv('Voting_sentiment_analysis_sclassification.csv', index=False)

    def to_polarity_classification(self):
        read = pd.read_csv("data_privacy_sentiment_analysis.csv")  # reads in CSV file
        new_column = pd.DataFrame()  # selects the text column and puts it into a data frame
        new_column.insert(0, 'followers count', read['followers count'])  # inserts column called followers count into the data frame
        new_column.insert(1, 'friends count', read['friends count'])  # inserts column called followers count into the data frame
        new_column.insert(2, 'retweet count', read['retweet count'])
        new_column.insert(3, 'favorite count', read['favorite count'])
        new_column.insert(4, 'subjectivity', read['subjectivity'])
        new_column.insert(5, 'PolarityClass', read['PolarityClass'])
        new_column.to_csv('Voting_sentiment_analysis_pclassification.csv', index=False)


if __name__ == "__main__":
    analysis = Analysis()
    analysis.polarity_and_subjectivity()
    analysis.polarity_class()
    analysis.subjectivity_class()
    analysis.to_subjectivity_classification()
    analysis.to_polarity_classification()
    analysis.scatter_plot()
    analysis.line_plot()
    analysis.hist_plot()
