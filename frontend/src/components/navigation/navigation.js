
import {
    SideNav, SideNavItems, SideNavLink, HeaderName, Header, SkipToContent
  } from "@carbon/react";
  import {
    Fork,
    Chat,
    Watson
  } from "@carbon/icons-react";
// import { background } from "@carbon/themes";
  
  function Navigation() {
     return (<>
         {/* <Header aria-label="Platform Name">
      <SkipToContent />
      <HeaderName href="#" prefix="">
        [Platform]
      </HeaderName>
      </Header> */}
      <SideNav aria-label="Side navigation" isRail style={{background: 'var(--surface-primary)', borderRight: '1px solid var(--border-strong, #1f3b5c)'}} isFixedNav expanded={true} isChildOfHeader={false}>
        <SideNavItems>
          <SideNavLink
            renderIcon={Watson}
            href="/">
              Wardrobe Planner
          </SideNavLink>
          
        </SideNavItems>
        <div className="footer" style={{padding: '1rem'}}>
           <p style={{marginBottom: '0.5rem'}}>Powered by <strong>ChatGPT</strong> © 2025 </p>           
           {/* <img src="https://upload.wikimedia.org/wikipedia/commons/1/1a/ChatGPT_logo.svg" alt="ChatGPT Logo" style={{height: '15px', 'margin': '0 10px'}}/> */}
         </div>
      </SideNav>;
    </>
    );
    
  }
  
  export default Navigation;
