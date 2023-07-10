# Task 1: Infrastructure

Solutions/suggestions to the first task are presented in this readme. Instead of presenting a single configuration for each situation, I chose to lay out multiple possible approaches that could be chosen from.

## Internal monitoring

```
In the Russia project, we run processes on a daily basis and need to know whether they have run successfully or not. Please suggest one or several configurations that would allow us (internally) to check the success of each process. We are looking for setups that are both easy to maintain and generate as little friction / efforts as possible for us to check
```

### Option 1: Store process logs in a database

The most flexible and lightweight option is to store simplified process logs in a database. Extending the existing API or creating a new dedicated one for receiving process logs should be simple. Internal users can access these logs either from the cloud or a local database client. It was mentioned in the interview that you are already using a PostgreSQL database, which should be a suitable place for these logs. If a more flexible structure is required, a separate NoSQL database could be used. However if the purpose is simply to report something like timestamps, process names, and process states then a relational database will do the job just fine.

Pros:
- Easy to setup
- Easy to maintain

Cons:
- Users need to have the skills and tools to use databases, especially if they are looking for specific process runs from a large amount of data
- This setup is not efficient for storing more detailed information like large error messages or stack traces. This solution is only good for checking the success of each process, not why it failed.

### Option 2: Use a dedicated logging and observability tool

For a more user-friendly and feature-rich approach, I would suggest using a dedicated logging and observability tool. Personally I have used a tool called Splunk, but a quick Google search shows many (open-source!) alternatives like SigNoz, Logstash and Fluentd. All of these provide a visual user interface and high customizability.

Pros:
- Feature rich
- Friendly for non-tech users
- High level of detail
- Logs can have complex structures

Cons:
- More setup
- More maintenance
- Probably overkill when it comes to features if the goal is to simply monitor whether processes have succeeded or not

## External alerts

```
External users of our platform should be able to set alerts for when potential fraudulent shipments are detected. Assuming the shipments are created in bulk and stored in a Postgres database query, design an infrastructure that would allow user to create / edit alert criteria and receive them when our system detects them. Please describe the setup in detail.
```

