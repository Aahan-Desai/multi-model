type ImagePreviewProps = {
  src: string;
  alt: string;
};

export function ImagePreview({ src, alt }: ImagePreviewProps) {
  return (
    <img
      src={src}
      alt={alt}
      className="h-36 w-full rounded-2xl object-cover"
    />
  );
}
