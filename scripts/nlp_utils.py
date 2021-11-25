import nltk.corpus
import bs4
import numpy
import pandas
import re
import json

STOPWORDS = set(nltk.corpus.stopwords.words('english'))  # a list of stopwords
CMU_DICT = nltk.corpus.cmudict.dict()  # a dictionary of English


def add_wordlist_cols(df, text_col='text', terms_json='../constants/terms.json'):
    """
    Given a dataframe with a column containing text and a JSON of variables and associated term wordlists, return the
    dataframe with additional columns for each variable with values being the words found in each text.

    Args:
         df         -- the ambient dataframe
         text_col   -- the name of the column containing the text to analyse
         terms_json -- the path to a JSON file of variables and associated terms
    """
    with open(terms_json, 'r') as f:
        term_dict = json.load(f)
        return pandas.concat([df, pandas.DataFrame(list(df[text_col].apply(lambda x: _extract_terms(x, term_dict))), index=df.index)], axis=1)


def get_wordlists_for_text(text, terms_json='../constants/terms.json'):
    """
    Given a single text string and a JSON of variables and associated term wordlists, return a dictionary with each
    variable and the corresponding terms from each wordlist found in the text.

    Args:
         text       -- input string to analyse
         terms_json -- the path to a JSON file of variables and associated terms
    """
    with open(terms_json, 'r') as f:
        term_dict = json.load(f)
        return _extract_terms(text, term_dict)


def _extract_terms(text, term_dict):
    """
    Given a text and a dictionary of variables and associated term wordlists, return a dictionary with the words found
    in the text for each variable.

    Args:
         text      -- text to analyse
         term_dict -- a dictionary with keys being the variables and values being lists of associated words
    """
    return {t: [x for x in term_dict[t] if (len(re.findall("\\b{}\\b".format(str(x.lower())), text.lower())) > 0)] for t in term_dict}


def bigram(words):
    return [f"{w} {words[i + 1] if i + 1 < len(words) else '#'}" for i, w in enumerate(words)]


def get_words(story, min_count=2):
    """
    From a (scraped) text, get the word tokens without stopwords and out of vocabulary words.

    Args:
        story: html-type text (string)
        min_count: the minimum number of documents that per type
        (set min_count=100 to only run the experiment on the most frequent catrgory; everything else will
        be "unknown")
    """
    # replace the html whitespaces with actual newlines
    soup = bs4.BeautifulSoup(story.encode().decode('unicode_escape'), 'html.parser')
    text = soup.text
    # take only words/numbers
    pattern = re.compile(r'\w+')
    words = pattern.findall(text)
    # exclude stopwords
    words = [w.lower() for w in words if len(w) > min_count and w not in STOPWORDS]
    # exclude weird words that are not in cmu dict
    words = [w for w in words if w in CMU_DICT]
    return words


def get_df(texts_data, ngram_type='unigram'):
    """
    From a set of texts, extract all the unique words and counts and fill them into a
    sparse data frame which can be used for bag of words modelling.

    Args:
        texts_data: the data frame containing the text in one field called "story"
        ngram_type: 'bigram' or 'unigram'; which ngram type to use (set to 'bigram' to run the bigram experiment)
    """
    counts_dict = {}
    for i in range(len(texts_data)):
        story = texts_data.loc[i, "story"]
        words = get_words(story)
        if ngram_type == 'bigram':
            words = bigram(words)
        unique, counts = numpy.unique(words, return_counts=True)
        counts_dict[texts_data.loc[i, "id"]] = {u: c for u, c in zip(unique, counts)}
    df = pandas.DataFrame.from_dict(counts_dict).T
    df = df.fillna(0)
    return df


def get_tokenized_words(tokenizer, story):
    """
    From a (scraped) text, get the word tokens without stopwords and out of vocabulary words.

    Args:
        tokenizer: tokenizer to use
        story: html-type text (string)
    """
    # replace the html whitespaces with actual newlines
    soup = bs4.BeautifulSoup(story.encode().decode('unicode_escape'), 'html.parser')
    text = soup.text
    # split on sentences, since that's the BERT way to do it
    sentences = []
    segment_ids = []
    for sentence in re.split(r'[\?\.\!\;\n]', text):
        marked_text = "[CLS] " + sentence + " [SEP]"
        tokenized_text = tokenizer.tokenize(marked_text)
        # the maximum sequence length for this model is 512; so we need to split longer sentences
        if len(tokenized_text) > 512:
            tokenized_text = [tokenized_text[:512], tokenized_text[512:]]
        else:
            tokenized_text = [tokenized_text]
        for tok in tokenized_text:
            indexed_tokens = tokenizer.convert_tokens_to_ids(tok)
            seg_id = [1] * len(tok)
            sentences.append(indexed_tokens)
            segment_ids.append(seg_id)
    return sentences, segment_ids
