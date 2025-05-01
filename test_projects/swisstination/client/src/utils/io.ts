export function debounce(func: any, timeout = 300) {
  let timer: any;
  return (...args: any) => {
    clearTimeout(timer);
    timer = setTimeout(() => {
      // @ts-ignore
      func.apply(null, args);
    }, timeout);
  };
}
