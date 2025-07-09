import React, { useEffect, useState } from 'react';
import GNB from '../GNB';
import { Outlet, useLocation } from 'react-router-dom';
import styles from './Layout.module.scss';
import Sidebar from '../Sidebar/Sidebar';
import Footer from '../Footer/index';
import { useSelector } from 'react-redux';
import { RootState } from '../../store';
import Loading from '../../pages/Loading';
import { WorkStatus } from './WorkStatus/WorkStatus';
import MainFooter from 'components/Footer/MainFooter';
import Navbar from 'components/Navbar';

const MOBILE_BREAKPOINT = 768;
const TABLET_BREAKPOINT = 1024;
const Layout: React.FC = () => {
  const user = useSelector((state: RootState) => state.auth.user);
  const location = useLocation();
  const isHomePage = location.pathname.includes('home');

  const [isMobile, setIsMobile] = useState(
    window.innerWidth < MOBILE_BREAKPOINT,
  );
  const [isTablet, setIsTablet] = useState(
    window.innerWidth < TABLET_BREAKPOINT &&
      window.innerWidth >= MOBILE_BREAKPOINT,
  );

  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  useEffect(() => {
    const handleResize = () => {
      const currentWidth = window.innerWidth;

      setIsMobile(currentWidth < MOBILE_BREAKPOINT);
      setIsTablet(
        currentWidth < TABLET_BREAKPOINT && currentWidth >= MOBILE_BREAKPOINT,
      );
      if (currentWidth >= TABLET_BREAKPOINT) {
        setIsSidebarOpen(false);
      }
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);
  const toggleSidebar = () => {
    setIsSidebarOpen((prev) => !prev);
  };

  return (
    <div className={styles['layout']}>
      {!isMobile && !isTablet && <Sidebar />}
      {(isMobile || isTablet) && (
        <>
          <button
            className={styles['hamburger-button']}
            onClick={toggleSidebar}
          >
            {isSidebarOpen ? '✖' : '☰'}
          </button>
          {isSidebarOpen && <Sidebar isMobile={true} onClose={toggleSidebar} />}
        </>
      )}

      <div className={styles['main']}>
        <Navbar userProfileUrl={''} />
        <div className={styles['content']}>
          <Outlet />
        </div>
      </div>
      {!isHomePage && <Footer />}
      {isHomePage && <MainFooter />}
    </div>
  );
};

export default Layout;
