<!-- README.html -->

<p><a href="https://jaffulee.github.io/Jaffulee/">Visit my website</a></p>

<h1>bike-points-api</h1>

<p><strong>TfL BikePoint API Extraction Pipeline</strong><br>
Automated extraction and loading of London bike point availability data for downstream analytics.</p>

<ul>
  <li>GitHub: <a href="https://github.com/Jaffulee">https://github.com/Jaffulee</a></li>
  <li>LinkedIn: <a href="https://www.linkedin.com/in/jeffrey-brian-thompson/">https://www.linkedin.com/in/jeffrey-brian-thompson/</a></li>
  <li>Writing: <a href="https://www.thedataschool.co.uk/blog/jeffrey-brian-thompson/">https://www.thedataschool.co.uk/blog/jeffrey-brian-thompson/</a></li>
</ul>

<hr>

<h2>About</h2>

<p>
This project extracts <strong>bike point availability data</strong> from the
<strong>Transport for London (TfL) BikePoint API</strong>, writes the results as JSON files,
and uploads them to <strong>AWS S3</strong>.
</p>

<p>
It serves as a <strong>lightweight example of a Bronze ingestion layer</strong>, demonstrating
API extraction, cloud loading, and basic orchestration patterns.
</p>

<hr>

<h2>Downstream Usage</h2>

<p>
While this repository focuses on extraction and loading only, the data produced here
is designed to feed a downstream analytics layer.
</p>

<p>
In my wider project ecosystem, similar raw datasets are modelled and transformed in:
</p>

<ul>
  <li>
    <strong>dbt analytics layer:</strong>
    <a href="https://github.com/Jaffulee/dbt-cloud-deng3">
      https://github.com/Jaffulee/dbt-cloud-deng3
    </a>
  </li>
</ul>

<p>
There, raw API data is transformed using a <strong>Medallion Architecture (Bronze → Silver → Gold)</strong>
into analytics-ready models.
</p>

<hr>

<h2>Features</h2>

<ul>
  <li>Extracts live bike point data from the TfL BikePoint API</li>
  <li>Writes API responses to local JSON files</li>
  <li>Uploads extracted data to Amazon S3</li>
  <li>Deletes local files after successful upload</li>
  <li>Simple, repeatable extraction pattern suitable for scheduling</li>
</ul>

<hr>

<h2>Project Structure</h2>

<pre>
├── main.py                               # Pipeline entry point
├── output_bike_json_files.py             # API extraction and JSON output
├── load_bike_json_s3.py                  # S3 upload and cleanup logic
├── kestra_beeikepoint_github_action_refactor.yml  # Orchestration proof of concept
├── requirements.txt                      # Python dependencies
├── schema_example.sql                    # Example downstream schema
└── README.md
</pre>

<hr>

<h2>How It Works</h2>

<h3>Step 1: Extract Bike Point Data</h3>

<p>
The pipeline calls the TfL BikePoint API and retrieves the latest availability and
station metadata for London bike points.
</p>

<h3>Step 2: Write JSON Files</h3>

<p>
API responses are written to JSON files, preserving the raw structure returned by the API.
</p>

<h3>Step 3: Upload to S3</h3>

<p>
JSON files are uploaded to an S3 bucket. After a successful upload, local copies are deleted.
</p>

<hr>

<h2>Configuration</h2>

<p>
AWS credentials are provided via a <code>.env</code> file:
</p>

<pre>
Access_key_ID=your_aws_access_key
Secret_access_key=your_aws_secret_key
AWS_BUCKET_NAME=your_target_bucket_name
</pre>

<hr>

<h2>Orchestration & SQL (Proof of Concept)</h2>

<p>
This repository includes:
</p>

<ul>
  <li>A <strong>Kestra orchestration example</strong> showing how the pipeline could be scheduled</li>
  <li>An <strong>example SQL silver-layer script</strong> illustrating downstream transformations</li>
</ul>

<p>
These components are included for <strong>demonstration purposes only</strong>.
The Kestra example uses unencrypted key–value stores and is <strong>not intended for production use</strong>.
</p>

<hr>

<h2>Notes</h2>

<ul>
  <li>This project applies <strong>no transformations or business logic</strong>.</li>
  <li>It focuses purely on API extraction and loading.</li>
  <li>All analytics modelling is assumed to occur downstream.</li>
</ul>
