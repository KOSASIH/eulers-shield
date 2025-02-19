import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Dashboard from './components/Dashboard';

const App = () => {
    return (
        <Router>
            <Navbar />
            <Switch>
                <Route path="/" exact component={Home} />
                <Route path="/dashboard" component={Dashboard} />
            </Switch>
        </Router>
    );
};

export default App;
