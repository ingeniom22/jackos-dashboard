import React from 'react';
import Sidebar from '../Sidebar/Sidebar';

const Layout = () => {
    return (
        <div className='grid grid-cols-12 gap-2 w-full h-full'>
            <Sidebar />
        </div>
    );
};

export default Layout;
