import React from 'react';
import Header from './components/Header';
import AboutMe from './components/AboutMe';
import Footer from './components/Footer';
import './App.css';

function App() {
  return (
    <div className="App">
      <Header />
      <main>
        <AboutMe />
        {/* Projects will go here later */}
      </main>
      <Footer />
    </div>
  );
}

export default App;