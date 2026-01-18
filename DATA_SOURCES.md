# Data Sources for Research Agent

A curated list of free, publicly accessible sources for documents and datasets.

## 📚 Research Papers & Academic Content

### ArXiv (Best for AI/ML/Physics/Math papers)
- **URL**: https://arxiv.org
- **Format**: PDF
- **Download Pattern**: `https://arxiv.org/pdf/[paper-id].pdf`
- **Examples**:
  ```bash
  # Attention Is All You Need (Transformers)
  python main.py download --url https://arxiv.org/pdf/1706.03762.pdf --auto-ingest

  # BERT
  python main.py download --url https://arxiv.org/pdf/1810.04805.pdf --auto-ingest

  # GPT-3
  python main.py download --url https://arxiv.org/pdf/2005.14165.pdf --auto-ingest
  ```
- **Categories**: AI, ML, CS, Physics, Math, Statistics

### PubMed Central (Medical/Biology papers)
- **URL**: https://www.ncbi.nlm.nih.gov/pmc/
- **Format**: PDF, TXT, XML
- **Free full-text biomedical and life sciences articles**

### Semantic Scholar
- **URL**: https://www.semanticscholar.org
- **Format**: PDF (when available)
- **Multi-disciplinary research papers**

### Google Scholar
- **URL**: https://scholar.google.com
- **Many papers link to free PDFs**

---

## 📖 Books & Literature

### Project Gutenberg (70,000+ free ebooks)
- **URL**: https://www.gutenberg.org
- **Format**: TXT, HTML, EPUB, PDF
- **Download Pattern**: `https://www.gutenberg.org/files/[book-id]/[book-id]-0.txt`
- **Examples**:
  ```bash
  # Pride and Prejudice
  python main.py download --url https://www.gutenberg.org/files/1342/1342-0.txt --filename pride_and_prejudice.txt --auto-ingest

  # Moby Dick
  python main.py download --url https://www.gutenberg.org/files/2701/2701-0.txt --filename moby_dick.txt --auto-ingest

  # Alice in Wonderland
  python main.py download --url https://www.gutenberg.org/files/11/11-0.txt --filename alice_in_wonderland.txt --auto-ingest
  ```
- **Note**: Public domain books only

### Internet Archive
- **URL**: https://archive.org
- **Millions of free books, movies, music**
- **Format**: Multiple formats

### Open Library
- **URL**: https://openlibrary.org
- **Free digital library**

---

## 📄 Documentation & Technical Manuals

### Python Documentation
```bash
# Python 3.11 PDF docs
python main.py download --url https://docs.python.org/3/archives/python-3.11.0-docs-pdf-a4.zip
```

### MDN Web Docs
- **URL**: https://developer.mozilla.org
- **Web development documentation**

### TensorFlow Documentation
```bash
python main.py download --url https://github.com/tensorflow/docs/archive/refs/heads/master.zip
```

### Django Documentation
```bash
python main.py download --url https://media.readthedocs.org/pdf/django/latest/django.pdf --auto-ingest
```

---

## 🌐 Wikipedia & Encyclopedias

### Wikipedia Articles (PDF)
- **API**: `https://en.wikipedia.org/api/rest_v1/page/pdf/[Article_Name]`
- **Examples**:
  ```bash
  # Machine Learning article
  python main.py download --url "https://en.wikipedia.org/api/rest_v1/page/pdf/Machine_learning" --filename machine_learning.pdf --auto-ingest

  # Artificial Intelligence
  python main.py download --url "https://en.wikipedia.org/api/rest_v1/page/pdf/Artificial_intelligence" --filename ai.pdf --auto-ingest
  ```

### Wikipedia Database Dumps
- **URL**: https://dumps.wikimedia.org
- **Entire Wikipedia in XML/SQL format**

---

## 📊 Datasets

### Kaggle Datasets
- **URL**: https://www.kaggle.com/datasets
- **Requires account (free)**
- **CSV, JSON, etc.**
- **Topics**: ML, data science, competitions

### UCI Machine Learning Repository
- **URL**: https://archive.ics.uci.edu/ml/
- **Classic ML datasets**

### Data.gov
- **URL**: https://data.gov
- **US Government open data**
- **CSV, JSON, XML**

### Google Dataset Search
- **URL**: https://datasetsearch.research.google.com
- **Search engine for datasets**

### Papers With Code Datasets
- **URL**: https://paperswithcode.com/datasets
- **ML/AI datasets linked to papers**

---

## 📰 News & Articles

### Common Crawl
- **URL**: https://commoncrawl.org
- **Web crawl data**
- **Petabytes of web data**

### News API
- **URL**: https://newsapi.org
- **News articles from various sources**
- **Free tier available**

---

## 🎓 Educational Resources

### MIT OpenCourseWare
- **URL**: https://ocw.mit.edu
- **Free MIT course materials**
- **Lecture notes, assignments, exams**

### Coursera (Free lectures)
- **URL**: https://www.coursera.org
- **Audit courses for free**

### Khan Academy
- **URL**: https://www.khanacademy.org
- **Educational videos and articles**

---

## 💻 Code & Repositories

### GitHub README files
- **Pattern**: `https://raw.githubusercontent.com/[user]/[repo]/main/README.md`
- **Examples**:
  ```bash
  # LangChain README
  python main.py download --url https://raw.githubusercontent.com/langchain-ai/langchain/master/README.md --auto-ingest

  # React README
  python main.py download --url https://raw.githubusercontent.com/facebook/react/main/README.md --auto-ingest
  ```

### GitHub Gists
- **URL**: https://gist.github.com
- **Code snippets and notes**

---

## 🔬 Scientific Data

### NASA Open Data
- **URL**: https://data.nasa.gov
- **Space and earth science data**

### European Space Agency
- **URL**: https://www.esa.int/ESA_Multimedia/Sets
- **Space mission data**

### CERN Open Data
- **URL**: http://opendata.cern.ch
- **Particle physics data**

---

## 🏛️ Historical & Government Documents

### US National Archives
- **URL**: https://www.archives.gov
- **Historical documents**

### Library of Congress
- **URL**: https://www.loc.gov
- **Digital collections**

### Europeana
- **URL**: https://www.europeana.eu
- **European cultural heritage**

---

## 📝 Curated Collections

### Awesome Public Datasets
- **URL**: https://github.com/awesomedata/awesome-public-datasets
- **Curated list of datasets by topic**

### Reddit Datasets
- **URL**: https://www.reddit.com/r/datasets/
- **Community-shared datasets**

---

## 🎯 Recommended Starting Collections

### For AI/ML Research:
```bash
# Download top AI papers
python main.py download --url \
  https://arxiv.org/pdf/1706.03762.pdf \
  https://arxiv.org/pdf/1810.04805.pdf \
  https://arxiv.org/pdf/2005.14165.pdf \
  https://arxiv.org/pdf/1409.0473.pdf \
  --auto-ingest
```

### For General Knowledge:
```bash
# Download classic books
python main.py download --url \
  https://www.gutenberg.org/files/1342/1342-0.txt \
  https://www.gutenberg.org/files/2701/2701-0.txt \
  https://www.gutenberg.org/files/11/11-0.txt \
  --auto-ingest
```

### For Technical Documentation:
```bash
# Download Python & Django docs
python main.py download --url \
  https://media.readthedocs.org/pdf/django/latest/django.pdf \
  --auto-ingest
```

### For Wikipedia Knowledge:
```bash
# Download Wikipedia articles
python main.py download --url \
  "https://en.wikipedia.org/api/rest_v1/page/pdf/Machine_learning" \
  "https://en.wikipedia.org/api/rest_v1/page/pdf/Artificial_intelligence" \
  "https://en.wikipedia.org/api/rest_v1/page/pdf/Natural_language_processing" \
  --auto-ingest
```

---

## 💡 Tips for Finding More Sources

1. **Search for "[topic] dataset public"** on Google
2. **Check university websites** - many publish research data
3. **Look for "awesome-[topic]" lists** on GitHub
4. **Use Google Dataset Search**
5. **Check API directories** like RapidAPI
6. **Government open data portals** by country
7. **Academic institution repositories**

---

## ⚠️ Important Notes

- **Copyright**: Only download content you have rights to use
- **Attribution**: Credit sources appropriately
- **Terms of Service**: Follow each source's ToS
- **Rate Limiting**: Don't overload servers
- **Storage**: Large datasets need significant disk space
- **Privacy**: Don't download/store personal data without consent

---

## 🚀 Quick Start Examples

### Build an AI Research Assistant:
```bash
# Download latest AI papers
python main.py download --url \
  https://arxiv.org/pdf/2303.08774.pdf \
  https://arxiv.org/pdf/2307.09288.pdf \
  --auto-ingest

# Query the agent
python main.py query "What are the latest developments in large language models?"
```

### Build a Literature Expert:
```bash
# Download classic literature
python main.py download --url \
  https://www.gutenberg.org/files/1342/1342-0.txt \
  https://www.gutenberg.org/files/84/84-0.txt \
  --auto-ingest

# Query the agent
python main.py query "Compare the writing styles in Pride and Prejudice and Frankenstein"
```

### Build a Tech Documentation Bot:
```bash
# Download documentation
python main.py download --url \
  https://raw.githubusercontent.com/langchain-ai/langchain/master/README.md \
  https://raw.githubusercontent.com/facebook/react/main/README.md \
  --auto-ingest

# Query the agent
python main.py query "How do I use LangChain with React?"
```
