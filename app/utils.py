# log tracing
def trace(st, col2, label, message):
    with col2:
        with st.expander(f"{label}:"):
            st.write(message)
