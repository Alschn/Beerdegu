import {useEffect, useState} from 'react';

const DEFAULT_VALUE_MS = 500;

function useDebounce<T>(value: T, delay: number = DEFAULT_VALUE_MS): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);

    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}

export default useDebounce;
