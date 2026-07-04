/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   init.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: Tsellak <tsellak@student.1337.ma>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/29 08:58:37 by Tsellak           #+#    #+#             */
/*   Updated: 2026/07/04 16:08:52 by Tsellak          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	init_dongle(t_data *data, int i)
{
	if (pthread_mutex_init(&data->dongles[i].mutex, NULL) != 0
		|| pthread_cond_init(&data->dongles[i].cond, NULL) != 0)
		return (1);
	data->dongles[i].in_use = 0;
	data->dongles[i].release_time = 0;
	data->dongles[i].tail = 0;
	data->dongles[i].queue = malloc(sizeof(t_coder *) * data->num_coders);
	return (!data->dongles[i].queue);
}

static int	init_coder(t_data *data, int i)
{
	if (pthread_mutex_init(&data->coders[i].state_mutex, NULL) != 0)
		return (1);
	data->coders[i].id = i + 1;
	data->coders[i].last_compile_start = data->start_time;
	data->coders[i].deadline = data->start_time + data->time_to_burnout;
	data->coders[i].compile_count = 0;
	data->coders[i].left_dongle = i;
	data->coders[i].right_dongle = (i + 1) % data->num_coders;
	data->coders[i].data = data;
	return (0);
}

static int	init_ressource(t_data *data)
{
	int	i;

	i = 0;
	while (i < data->num_coders)
	{
		if (init_dongle(data, i))
		{
			while (--i >= 0)
				free(data->dongles[i].queue);
			return (1);
		}
		if (init_coder(data, i))
		{
			while (--i >= 0)
				free(data->dongles[i].queue);
			return (1);
		}
		i++;
	}
	return (0);
}

static int	init_simulation(t_data *data)
{
	data->start_time = get_time_ms();
	data->simulation_end = 0;
	data->dongles = malloc(sizeof(t_dongle) * data->num_coders);
	data->coders = malloc(sizeof(t_coder) * data->num_coders);
	if (!data->dongles || !data->coders)
		return (1);
	if (init_ressource(data) != 0)
		return (1);
	if (pthread_mutex_init(&data->print_mutex, NULL) != 0
		|| pthread_mutex_init(&data->state_mutex, NULL) != 0)
		return (1);
	return (0);
}

int	start_threads(t_data *data)
{
	int	i;

	if (init_simulation(data))
		return (1);
	i = 0;
	while (i < data->num_coders)
	{
		if (pthread_create(&data->coders[i].thread, NULL, coder_routine,
				&data->coders[i]) != 0)
			ft_exit("Error creating coder thread\n", NULL, NULL);
		i++;
	}
	if (pthread_create(&data->monitor, NULL, monitor_routine, data) != 0)
		ft_exit("Error creating monitor thread\n", NULL, NULL);
	i = 0;
	while (i < data->num_coders)
	{
		pthread_join(data->coders[i].thread, NULL);
		i++;
	}
	pthread_join(data->monitor, NULL);
	return (0);
}
