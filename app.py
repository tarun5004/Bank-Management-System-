"""
Bank Management System - Streamlit Web Application

This module provides a web-based interface for the Bank Management System
using Streamlit with proper session management and user experience.
"""

import streamlit as st
from bank import (
    Bank,
    BankError,
    AccountNotFoundError,
    AuthenticationError,
    ValidationError,
    InsufficientFundsError
)


# Page configuration
st.set_page_config(
    page_title="Bank Management System",
    page_icon="🏦",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'bank' not in st.session_state:
    st.session_state.bank = Bank()

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'current_account' not in st.session_state:
    st.session_state.current_account = None

if 'current_pin' not in st.session_state:
    st.session_state.current_pin = None


def logout():
    """Clear session state for logout."""
    st.session_state.logged_in = False
    st.session_state.current_account = None
    st.session_state.current_pin = None


def mask_account_number(account_no: str) -> str:
    """Mask account number for display (show first 3 and last 2 characters)."""
    if len(account_no) > 5:
        return account_no[:3] + "***" + account_no[-2:]
    return account_no


def home_page():
    """Render the home/welcome page."""
    st.title("🏦 Bank Management System")
    st.markdown("---")
    
    st.markdown("""
    Welcome to our **Bank Management System**! 
    
    This secure platform allows you to manage your banking needs with ease.
    
    ### Features:
    - 📝 **Create Account** - Open a new bank account
    - 💰 **Deposit** - Add funds to your account
    - 💸 **Withdraw** - Withdraw funds from your account
    - 📊 **View Details** - Check your account information
    - ✏️ **Update Details** - Modify your account information
    - 🗑️ **Delete Account** - Close your account
    
    ### Getting Started:
    Use the sidebar to navigate between different services.
    """)
    
    st.info("💡 **Tip:** Your PIN is securely hashed and stored. Never share your PIN with anyone!")


def create_account_page():
    """Render the create account page."""
    st.title("📝 Create New Account")
    st.markdown("---")
    
    with st.form("create_account_form"):
        st.subheader("Personal Information")
        
        name = st.text_input(
            "Full Name",
            placeholder="Enter your full name",
            help="Name should contain only letters and spaces"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input(
                "Age",
                min_value=1,
                max_value=120,
                value=18,
                help="You must be at least 18 years old"
            )
        
        with col2:
            email = st.text_input(
                "Email",
                placeholder="example@email.com",
                help="Enter a valid email address"
            )
        
        pin = st.text_input(
            "4-Digit PIN",
            type="password",
            max_chars=4,
            placeholder="****",
            help="Create a 4-digit PIN for your account"
        )
        
        confirm_pin = st.text_input(
            "Confirm PIN",
            type="password",
            max_chars=4,
            placeholder="****",
            help="Re-enter your PIN"
        )
        
        submitted = st.form_submit_button("Create Account", use_container_width=True)
        
        if submitted:
            if pin != confirm_pin:
                st.error("❌ PINs do not match!")
            else:
                try:
                    with st.spinner("Creating your account..."):
                        result = st.session_state.bank.create_account(name, age, email, pin)
                    
                    st.success("✅ Account created successfully!")
                    st.balloons()
                    
                    st.markdown("### Your Account Details")
                    st.info(f"""
                    **Account Number:** `{result['accountNo']}`
                    
                    **Name:** {result['name']}
                    
                    **Email:** {result['email']}
                    
                    **Balance:** ₹{result['balance']:.2f}
                    """)
                    
                    st.warning("⚠️ **Important:** Please save your account number safely. You will need it for all transactions.")
                    
                except ValidationError as e:
                    st.error(f"❌ {e}")
                except BankError as e:
                    st.error(f"❌ Error: {e}")


def login_section():
    """Render the login section for authenticated operations."""
    st.subheader("🔐 Account Login")
    
    account_no = st.text_input(
        "Account Number",
        placeholder="Enter your account number",
        key="login_account"
    )
    
    pin = st.text_input(
        "PIN",
        type="password",
        max_chars=4,
        placeholder="****",
        key="login_pin"
    )
    
    if st.button("Login", use_container_width=True):
        if account_no and pin:
            # Verify credentials using public method
            if st.session_state.bank.verify_credentials(account_no, pin):
                st.session_state.logged_in = True
                st.session_state.current_account = account_no
                st.session_state.current_pin = pin
                st.success("✅ Logged in successfully!")
                st.rerun()
            else:
                st.error("❌ Invalid account number or PIN.")
        else:
            st.warning("Please enter both account number and PIN.")
    
    return None


def deposit_page():
    """Render the deposit page."""
    st.title("💰 Deposit Money")
    st.markdown("---")
    
    if not st.session_state.logged_in:
        login_section()
    else:
        st.success(f"Logged in as: {mask_account_number(st.session_state.current_account)}")
        
        if st.button("Logout", key="deposit_logout"):
            logout()
            st.rerun()
        
        st.markdown("---")
        
        with st.form("deposit_form"):
            amount = st.number_input(
                "Amount to Deposit (₹)",
                min_value=0.01,
                max_value=100000.0,
                value=100.0,
                step=100.0,
                help="Maximum deposit limit: ₹100,000"
            )
            
            submitted = st.form_submit_button("Deposit", use_container_width=True)
            
            if submitted:
                try:
                    with st.spinner("Processing deposit..."):
                        result = st.session_state.bank.deposit(
                            st.session_state.current_account,
                            st.session_state.current_pin,
                            amount
                        )
                    
                    st.success("✅ Deposit successful!")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Deposited", f"₹{result['deposited']:.2f}")
                    with col2:
                        st.metric("New Balance", f"₹{result['new_balance']:.2f}")
                        
                except ValidationError as e:
                    st.error(f"❌ {e}")
                except (AccountNotFoundError, AuthenticationError) as e:
                    st.error(f"❌ {e}")
                    logout()
                    st.rerun()
                except BankError as e:
                    st.error(f"❌ Error: {e}")


def withdraw_page():
    """Render the withdraw page."""
    st.title("💸 Withdraw Money")
    st.markdown("---")
    
    if not st.session_state.logged_in:
        login_section()
    else:
        st.success(f"Logged in as: {mask_account_number(st.session_state.current_account)}")
        
        if st.button("Logout", key="withdraw_logout"):
            logout()
            st.rerun()
        
        st.markdown("---")
        
        # Show current balance
        try:
            details = st.session_state.bank.get_details(
                st.session_state.current_account,
                st.session_state.current_pin
            )
            st.info(f"💵 Current Balance: ₹{details['balance']:.2f}")
        except BankError:
            pass
        
        with st.form("withdraw_form"):
            amount = st.number_input(
                "Amount to Withdraw (₹)",
                min_value=0.01,
                value=100.0,
                step=100.0,
                help="You cannot withdraw more than your current balance"
            )
            
            submitted = st.form_submit_button("Withdraw", use_container_width=True)
            
            if submitted:
                try:
                    with st.spinner("Processing withdrawal..."):
                        result = st.session_state.bank.withdraw(
                            st.session_state.current_account,
                            st.session_state.current_pin,
                            amount
                        )
                    
                    st.success("✅ Withdrawal successful!")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Withdrawn", f"₹{result['withdrawn']:.2f}")
                    with col2:
                        st.metric("Remaining Balance", f"₹{result['new_balance']:.2f}")
                        
                except ValidationError as e:
                    st.error(f"❌ {e}")
                except InsufficientFundsError as e:
                    st.error(f"❌ {e}")
                except (AccountNotFoundError, AuthenticationError) as e:
                    st.error(f"❌ {e}")
                    logout()
                    st.rerun()
                except BankError as e:
                    st.error(f"❌ Error: {e}")


def details_page():
    """Render the account details page."""
    st.title("📊 Account Details")
    st.markdown("---")
    
    if not st.session_state.logged_in:
        login_section()
    else:
        st.success(f"Logged in as: {mask_account_number(st.session_state.current_account)}")
        
        if st.button("Logout", key="details_logout"):
            logout()
            st.rerun()
        
        st.markdown("---")
        
        try:
            with st.spinner("Fetching account details..."):
                details = st.session_state.bank.get_details(
                    st.session_state.current_account,
                    st.session_state.current_pin
                )
            
            st.subheader("Your Account Information")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Name:**")
                st.markdown("**Age:**")
                st.markdown("**Email:**")
                st.markdown("**Account Number:**")
                st.markdown("**PIN:**")
                st.markdown("**Balance:**")
            
            with col2:
                st.markdown(f"{details['name']}")
                st.markdown(f"{details['age']} years")
                st.markdown(f"{details['email']}")
                st.markdown(f"`{details['accountNo']}`")
                st.markdown(f"{details['pin']}")
                st.markdown(f"₹{details['balance']:.2f}")
            
            st.markdown("---")
            st.metric("Current Balance", f"₹{details['balance']:.2f}")
            
        except (AccountNotFoundError, AuthenticationError) as e:
            st.error(f"❌ {e}")
            logout()
            st.rerun()
        except BankError as e:
            st.error(f"❌ Error: {e}")


def update_page():
    """Render the update details page."""
    st.title("✏️ Update Details")
    st.markdown("---")
    
    if not st.session_state.logged_in:
        login_section()
    else:
        st.success(f"Logged in as: {mask_account_number(st.session_state.current_account)}")
        
        if st.button("Logout", key="update_logout"):
            logout()
            st.rerun()
        
        st.markdown("---")
        
        # Get current details
        try:
            current_details = st.session_state.bank.get_details(
                st.session_state.current_account,
                st.session_state.current_pin
            )
        except BankError:
            current_details = {"name": "", "email": ""}
        
        st.subheader("Update Your Information")
        st.info("Leave fields empty to keep current values.")
        
        with st.form("update_form"):
            new_name = st.text_input(
                "New Name",
                placeholder=f"Current: {current_details.get('name', '')}",
                help="Leave empty to keep current name"
            )
            
            new_email = st.text_input(
                "New Email",
                placeholder=f"Current: {current_details.get('email', '')}",
                help="Leave empty to keep current email"
            )
            
            st.markdown("---")
            st.markdown("**Change PIN**")
            
            new_pin = st.text_input(
                "New PIN",
                type="password",
                max_chars=4,
                placeholder="****",
                help="Leave empty to keep current PIN"
            )
            
            confirm_new_pin = st.text_input(
                "Confirm New PIN",
                type="password",
                max_chars=4,
                placeholder="****"
            )
            
            submitted = st.form_submit_button("Update Details", use_container_width=True)
            
            if submitted:
                if new_pin and new_pin != confirm_new_pin:
                    st.error("❌ New PINs do not match!")
                else:
                    try:
                        with st.spinner("Updating your details..."):
                            result = st.session_state.bank.update_details(
                                st.session_state.current_account,
                                st.session_state.current_pin,
                                name=new_name if new_name.strip() else None,
                                email=new_email if new_email.strip() else None,
                                new_pin=new_pin if new_pin else None
                            )
                        
                        st.success(f"✅ {result['message']}")
                        
                        # Update stored PIN if changed
                        if new_pin:
                            st.session_state.current_pin = new_pin
                            st.info("Your PIN has been updated. Please remember your new PIN.")
                        
                    except ValidationError as e:
                        st.error(f"❌ {e}")
                    except (AccountNotFoundError, AuthenticationError) as e:
                        st.error(f"❌ {e}")
                        logout()
                        st.rerun()
                    except BankError as e:
                        st.error(f"❌ Error: {e}")


def delete_page():
    """Render the delete account page."""
    st.title("🗑️ Delete Account")
    st.markdown("---")
    
    if not st.session_state.logged_in:
        login_section()
    else:
        st.success(f"Logged in as: {mask_account_number(st.session_state.current_account)}")
        
        if st.button("Logout", key="delete_logout"):
            logout()
            st.rerun()
        
        st.markdown("---")
        
        st.warning("⚠️ **Warning:** This action is irreversible. Your account and all associated data will be permanently deleted.")
        
        # Show current balance
        try:
            details = st.session_state.bank.get_details(
                st.session_state.current_account,
                st.session_state.current_pin
            )
            if details['balance'] > 0:
                st.error(f"⚠️ You have ₹{details['balance']:.2f} in your account. Please withdraw all funds before deleting.")
        except BankError:
            pass
        
        st.markdown("---")
        
        confirm_text = st.text_input(
            "Type 'DELETE' to confirm account deletion",
            placeholder="DELETE",
            help="This action cannot be undone"
        )
        
        if st.button("Delete My Account", type="primary", use_container_width=True):
            if confirm_text == "DELETE":
                try:
                    with st.spinner("Deleting your account..."):
                        result = st.session_state.bank.delete_account(
                            st.session_state.current_account,
                            st.session_state.current_pin
                        )
                    
                    st.success(f"✅ {result['message']}")
                    logout()
                    st.info("You have been logged out.")
                    
                except (AccountNotFoundError, AuthenticationError) as e:
                    st.error(f"❌ {e}")
                    logout()
                    st.rerun()
                except BankError as e:
                    st.error(f"❌ Error: {e}")
            else:
                st.error("❌ Please type 'DELETE' to confirm account deletion.")


def main():
    """Main function to run the Streamlit application."""
    # Sidebar navigation
    st.sidebar.title("🏦 Navigation")
    st.sidebar.markdown("---")
    
    pages = {
        "🏠 Home": home_page,
        "📝 Create Account": create_account_page,
        "💰 Deposit": deposit_page,
        "💸 Withdraw": withdraw_page,
        "📊 Account Details": details_page,
        "✏️ Update Details": update_page,
        "🗑️ Delete Account": delete_page
    }
    
    selection = st.sidebar.radio("Select a service:", list(pages.keys()))
    
    st.sidebar.markdown("---")
    
    # Show login status
    if st.session_state.logged_in:
        st.sidebar.success(f"✅ Logged in")
        st.sidebar.caption(f"Account: {mask_account_number(st.session_state.current_account)}")
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            logout()
            st.rerun()
    else:
        st.sidebar.info("Not logged in")
    
    st.sidebar.markdown("---")
    st.sidebar.caption("© 2024 Bank Management System")
    
    # Render selected page
    pages[selection]()


if __name__ == "__main__":
    main()
