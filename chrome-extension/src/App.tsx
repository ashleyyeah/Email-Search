import { useState } from 'react';
import { SearchResult } from './types';
import './App.css';

export default function App() {
  const [query, setQuery] = useState<string>('');
  const [result, setResult] = useState<Array<SearchResult>>([]);

  async function handleSubmit(e: any) {
    e.preventDefault();
    try {
      let res = await fetch(`http://localhost:5000/api/search?query=${encodeURIComponent(e.target.search.value)}`, {
        method: "GET",
      });
      let resJson = await res.json();
      if (res.status === 200) {
        setResult(resJson);
      }
    } catch (err) {
      console.log(err);
    }
  };

  const getEmail = (query: string, date: string) => {
    const queryInfo: chrome.tabs.QueryInfo = {
      active: true,
      currentWindow: true
    };

    chrome.tabs && chrome.tabs.query(queryInfo, function(tabs) {
      var tab = tabs[0];
      chrome.tabs.update(tab.id!, 
        {url: `https://mail.google.com/mail/u/0/#advanced-search/subject=${encodeURI(query)}&subset=all&within=1d&sizeoperator=s_sl&sizeunit=s_smb&date=${encodeURIComponent(date)}`});
    });
  };

  return (
    <div className="App">
      <header style={{ margin: 15 }} className="App-header">
        <h1>Email Search</h1>
        <form onSubmit={handleSubmit}>
          <div>
            <input
              type="text"
              name="search"
              placeholder="Search"
              value={query}
              style={{ marginRight: 10 }}
              onChange={(e) => setQuery(e.target.value)}
            />
            <button type="submit">Search</button>
          </div>
        </form>
        <dl style={{ textAlign: 'left', fontSize: '16px', width: '475px' }} >
          {result.map(function(item: SearchResult, i) {
            return (
              <span>
                <dt key={i}>{item.title}</dt>
                <dt key={i}>{item.date}</dt>
                <dd style={{
                    maxWidth: '475px',
                    marginBottom: 10 }} 
                  key={i}>{item.body}</dd>
                <button onClick={() => getEmail(item.title, item.date)}>Go to Email</button>
                <hr className="rounded"></hr>
              </span>
            );
          })}
        </dl>
      </header>
    </div>
  );
};
