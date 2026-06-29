/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   cleanup.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: Tsellak <tsellak@student.1337.ma>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/29 08:42:16 by Tsellak           #+#    #+#             */
/*   Updated: 2026/06/29 10:54:13 by Tsellak          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	cleanup_all(t_data *data)
{
	int	i;

	if (data->dongles)
	{
		i = 0;
		while (i < data->num_coders)
		{
			free(data->dongles[i].queue);
			pthread_mutex_destroy(&data->dongles[i].mutex);
			pthread_cond_destroy(&data->dongles[i].cond);
			pthread_mutex_destroy(&data->coders[i].state_mutex);
			i++;
		}
		free(data->dongles);
	}
	pthread_mutex_destroy(&data->print_mutex);
	pthread_mutex_destroy(&data->state_mutex);
	free(data->coders);
}
