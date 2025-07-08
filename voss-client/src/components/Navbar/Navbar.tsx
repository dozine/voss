import React from 'react';
import styles from './Navbar.module.scss';
import { WorkStatus } from 'components/Layout/WorkStatus/WorkStatus';
import GNB from 'components/GNB';

interface NavbarProps {
  userProfileUrl: string;
}

const Navbar: React.FC<NavbarProps> = ({ userProfileUrl }) => {
  return (
    <div className={styles.navbarWrapper}>
      <div className={styles.navbarInner}>
        <div className={styles.navbarLeft}>
          <WorkStatus />
        </div>
        <div className={styles.navbarRight}>
          <GNB userProfileUrl={userProfileUrl} />
        </div>
      </div>
    </div>
  );
};

export default Navbar;
