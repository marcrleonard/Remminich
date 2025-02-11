from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field

class SearchModel(BaseModel):
    checksum: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    createdAfter: Optional[str] = None
    createdBefore: Optional[str] = None
    description: Optional[str] = None
    deviceAssetId: Optional[str] = None
    deviceId: Optional[str] = None
    encodedVideoPath: Optional[str] = None
    id: UUID
    isArchived: Optional[bool] = None
    isEncoded: Optional[bool] = None
    isFavorite: Optional[bool] = None
    isMotion: Optional[bool] = None
    isNotInAlbum: Optional[bool] = None
    isOffline: Optional[bool] = None
    isVisible: Optional[bool] = None
    lensModel: Optional[str] = None
    libraryId: UUID
    make: Optional[str] = None
    model: Optional[str] = None
    order: Optional[str] = None
    originalFileName: Optional[str] = None
    originalPath: Optional[str] = None
    page: Optional[int] = None
    personIds: Optional[List[UUID]] = None
    previewPath: Optional[str] = None
    size: Optional[int] = None
    state: Optional[str] = None
    tagIds: Optional[List[UUID]] = None
    takenAfter: Optional[str] = None
    takenBefore: Optional[str] = None
    thumbnailPath: Optional[str] = None
    trashedAfter: Optional[str] = None
    trashedBefore: Optional[str] = None
    type: Optional[str] = None
    updatedAfter: Optional[str] = None
    updatedBefore: Optional[str] = None
    withArchived: Optional[bool] = None
    withDeleted: Optional[bool] = None
    withExif: Optional[bool] = None
    withPeople: Optional[bool] = None
    withStacked: Optional[bool] = None

    class Config:
        json_encoders = {
            UUID: str  # Ensure UUIDs are serialized as strings
        }
        exclude_none = True  # Exclude fields that are None from serialization
