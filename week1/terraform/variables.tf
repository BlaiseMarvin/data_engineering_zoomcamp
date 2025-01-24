variable "credentials" {
    description = "My Credentials"
    default = "../../keys.json"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default = "demo_dataset"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default = "STANDARD"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default = "total-fiber-448420-g2-dem_bucket"
}

variable "location" {
    description = "Project Location"
    default = "US"
}