from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field

# PATCH /albums/:id
class UpdateAlbumModel(BaseModel):
    albumName: Optional[str] = None
    albumThumbnailAssetId: Optional[str] = None
    description: Optional[str] = None
    isActivityEnabled: Optional[bool] = None
    order: Optional[str] = None

    class Config:
        json_exclude_none = True

# PUT /assets/:id
class SingleAssetUpdateModel(BaseModel):
    dateTimeOriginal: Optional[str] = None
    description: Optional[str] = None
    isArchived: Optional[bool] = None
    isFavorite: Optional[bool] = None
    latitude: Optional[float] = None
    livePhotoVideoId: Optional[str] = None
    longitude: Optional[float] = None
    rating: Optional[int] = None

    class Config:
        # json_encoders = {None: lambda v: v if v is not None else ...}
        json_exclude_none = True


# PUT /assets
class BulkUpdateAssetsModel(BaseModel):
    dateTimeOriginal: Optional[str] = None
    duplicateId: Optional[str] = None
    ids: List[str] = Field(..., min_items=1)
    isArchived: Optional[bool] = None
    isFavorite: Optional[bool] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    rating: Optional[int] = None


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