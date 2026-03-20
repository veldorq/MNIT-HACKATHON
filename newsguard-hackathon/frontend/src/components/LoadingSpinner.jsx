function LoadingSpinner({ size = "h-5 w-5" }) {
  return (
    <span
      className={`${size} inline-block animate-spin rounded-full border-2 border-white border-t-transparent`}
      aria-label="Loading"
      role="status"
    />
  );
}

export default LoadingSpinner;
