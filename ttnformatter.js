function decodeUplink(input) {
  const jsonStr = String.fromCharCode.apply(null, input.bytes);
  const data = JSON.parse(jsonStr);

  return {
    data: data,
    warnings: [],
    errors: []
  };
}
